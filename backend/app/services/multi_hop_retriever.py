from typing import List, Dict
from .vector_store import VectorStore

class MultiHopRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def retrieve(self, steps: List[Dict[str, str]]) -> Dict[str, List[Dict]]:
        results = {}
        for step in steps:
            query = step.get("query", "")
            results[query] = self.vector_store.search(query, top_k=5)
        return results
    
    def aggregate_context(self, retrieval_results: Dict[str, List[Dict]]) -> str:
        """Aggregate with better formatting and deduplication"""
        context = ""
        seen_chunks = set()
        
        for query, results in retrieval_results.items():
            context += f"\n## Retrieved for: {query}\n"
            
            for i, result in enumerate(results, 1):
                # Deduplicate by text hash
                text_hash = hash(result['text'][:100])
                if text_hash in seen_chunks:
                    continue
                seen_chunks.add(text_hash)
                
                source = result["metadata"].get("source", "Unknown")
                section = result["metadata"].get("section", "")
                score = result.get("combined_score", result.get("score", 0))
                
                context += f"\n[{i}] Source: {source}"
                if section:
                    context += f" | Section: {section}"
                context += f" | Relevance: {score:.2f}\n{result['text']}\n"
        
        return context
