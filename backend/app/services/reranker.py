from typing import List, Dict
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

class Reranker:
    """Rerank retrieved chunks using LLM for better relevance"""
    
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Score each passage's relevance to the query (0-10).
            
Consider:
- Direct answer to query
- Supporting evidence
- Context quality
            
Return scores as JSON: {{"scores": [8, 5, 9, ...]}}"""),
            ("user", "Query: {query}\n\nPassages:\n{passages}")
        ])
    
    def rerank(self, query: str, results: List[Dict], top_k: int = 5) -> List[Dict]:
        if not results:
            return []
        
        passages = "\n\n".join([
            f"[{i}] {r['text'][:500]}..." 
            for i, r in enumerate(results)
        ])
        
        try:
            response = self.llm.invoke(
                self.prompt.format_messages(query=query, passages=passages)
            )
            
            # Parse scores (simplified - in production use structured output)
            import json
            scores_data = json.loads(response.content)
            scores = scores_data.get("scores", [])
            
            # Combine with original scores
            for i, result in enumerate(results):
                if i < len(scores):
                    result["rerank_score"] = scores[i] / 10.0
                    result["combined_score"] = (result["score"] + result["rerank_score"]) / 2
            
            # Sort by combined score
            reranked = sorted(results, key=lambda x: x.get("combined_score", 0), reverse=True)
            return reranked[:top_k]
        
        except Exception as e:
            print(f"Reranking failed: {e}")
            return results[:top_k]
