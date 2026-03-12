from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from .agents.query_analyzer import QueryAnalyzerAgent
from .agents.retrieval_planner import RetrievalPlannerAgent
from .agents.self_evaluator import SelfEvaluationAgent
from .agents.answer_generator import AnswerGeneratorAgent
from .services.vector_store import VectorStore
from .services.multi_hop_retriever import MultiHopRetriever
from .services.document_processor import DocumentProcessor
from .services.reranker import Reranker
from .services.query_expansion import QueryExpander
from .services.citation_extractor import CitationExtractor
from .services.conversation_memory import ConversationMemory
from .config import Settings
from .models import Citation
import logging

logger = logging.getLogger(__name__)

class ResearchOrchestrator:
    def __init__(self, settings: Settings):
        self.llm = ChatOpenAI(
            model=settings.llm_model,
            api_key=settings.openai_api_key,
            temperature=0
        )
        
        # Agents
        self.query_analyzer = QueryAnalyzerAgent(self.llm)
        self.planner = RetrievalPlannerAgent(self.llm)
        self.evaluator = SelfEvaluationAgent(self.llm)
        self.answer_generator = AnswerGeneratorAgent(self.llm)
        
        # Core services
        self.vector_store = VectorStore(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            collection_name=settings.collection_name,
            embedding_model=settings.embedding_model
        )
        
        self.retriever = MultiHopRetriever(self.vector_store)
        self.processor = DocumentProcessor()
        
        # Advanced services
        self.reranker = Reranker(self.llm)
        self.query_expander = QueryExpander(self.llm)
        self.citation_extractor = CitationExtractor()
        self.memory = ConversationMemory()
        
        self.settings = settings
    
    async def process_question(
        self, 
        question: str, 
        session_id: Optional[str] = None,
        use_query_expansion: bool = True,
        use_reranking: bool = True
    ) -> Dict:
        """
        Advanced multi-hop RAG pipeline with query expansion, reranking, and self-evaluation
        """
        logger.info(f"Processing question: {question}")
        
        # Step 0: Handle follow-up questions
        if session_id:
            question = self.memory.resolve_followup(session_id, question)
        
        # Step 1: Analyze query
        analysis = self.query_analyzer.analyze(question)
        logger.info(f"Query type: {analysis.query_type}, Multi-hop: {analysis.requires_multi_hop}")
        
        # Step 2: Query expansion for better retrieval
        expanded_queries = [question]
        if use_query_expansion and analysis.requires_multi_hop:
            expanded_queries = self.query_expander.expand(question)
            logger.info(f"Expanded to {len(expanded_queries)} queries")
        
        # Step 3: Create retrieval plan
        plan = self.planner.plan(question, analysis.sub_queries)
        
        # Step 4: Multi-hop retrieval with expansion
        retrieval_results = {}
        for step in plan.steps:
            step_query = step.get("query", "")
            
            # Retrieve with expanded queries
            all_results = []
            for exp_query in expanded_queries:
                combined_query = f"{step_query} {exp_query}"
                results = self.vector_store.search(combined_query, top_k=10)
                all_results.extend(results)
            
            # Deduplicate by chunk text
            seen_texts = set()
            unique_results = []
            for r in all_results:
                text_hash = hash(r["text"][:100])
                if text_hash not in seen_texts:
                    seen_texts.add(text_hash)
                    unique_results.append(r)
            
            # Rerank for relevance
            if use_reranking and unique_results:
                unique_results = self.reranker.rerank(step_query, unique_results, top_k=5)
            
            retrieval_results[step_query] = unique_results[:5]
        
        context = self.retriever.aggregate_context(retrieval_results)
        logger.info(f"Retrieved context: {len(context)} chars")
        
        # Step 5: Generate answer
        answer_text = self.answer_generator.generate(question, context)
        
        # Step 6: Extract and validate citations
        answer_with_refs, citations_raw = self.citation_extractor.extract_citations(
            answer_text, retrieval_results
        )
        citation_validation = self.citation_extractor.validate_citations(
            answer_with_refs, context
        )
        
        # Convert to Citation model
        citations = [Citation(**cit) for cit in citations_raw]
        
        # Step 7: Self-evaluation
        evaluation = self.evaluator.evaluate(question, answer_with_refs, context)
        logger.info(f"Confidence: {evaluation.confidence}, Support ratio: {citation_validation['support_ratio']}")
        
        # Step 8: Adaptive re-retrieval if needed
        if evaluation.confidence < 0.7 and evaluation.missing_info:
            logger.info("Low confidence, performing additional retrieval")
            
            for missing_topic in evaluation.missing_info[:2]:  # Limit to 2 additional queries
                extra_results = self.vector_store.search(missing_topic, top_k=3)
                
                if use_reranking:
                    extra_results = self.reranker.rerank(missing_topic, extra_results, top_k=3)
                
                if extra_results:
                    context += f"\n\n## Additional Context for '{missing_topic}':\n"
                    for r in extra_results:
                        context += f"{r['text']}\n\n"
            
            # Regenerate answer with additional context
            answer_text = self.answer_generator.generate(question, context)
            answer_with_refs, citations_raw = self.citation_extractor.extract_citations(
                answer_text, retrieval_results
            )
            citations = [Citation(**cit) for cit in citations_raw]
            
            # Re-evaluate
            evaluation = self.evaluator.evaluate(question, answer_with_refs, context)
        
        # Step 9: Store in conversation memory
        if session_id:
            self.memory.add_message(
                session_id, question, answer_with_refs, 
                [cit.model_dump() for cit in citations],
                metadata={"confidence": evaluation.confidence, "query_type": analysis.query_type}
            )
        
        return {
            "answer": answer_with_refs,
            "citations": citations,
            "confidence": evaluation.confidence,
            "retrieval_steps": plan.steps,
            "query_analysis": {
                "type": analysis.query_type,
                "requires_multi_hop": analysis.requires_multi_hop,
                "sub_queries": analysis.sub_queries
            },
            "validation": {
                "support_ratio": citation_validation["support_ratio"],
                "unsupported_claims": citation_validation["unsupported_claims"]
            }
        }
    
    def ingest_document(self, file_path: str, metadata: Dict):
        chunks = self.processor.process_pdf(file_path, metadata)
        self.vector_store.add_documents(chunks)
    
    def _extract_citations(self, retrieval_results: Dict) -> list:
        citations = []
        for query, results in retrieval_results.items():
            for result in results:
                source = result["metadata"].get("source", "Unknown")
                if source not in [c["source"] for c in citations]:
                    citations.append({
                        "source": source,
                        "relevance": result["score"]
                    })
        return citations
