from typing import List, Dict
from .vector_store import VectorStore

class MultiHopRetriever:
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
    
    def retrieve(self, retrieval_plan: List[Dict[str, str]], top_k: int = 3) -> Dict[str, List[Dict]]:
        results = {}
        for step in retrieval_plan:
            query = step.get("query", "")
            step_results = self.vector_store.search(query, top_k=top_k)
            results[query] = step_results
        return results
    
    def aggregate_context(self, retrieval_results: Dict[str, List[Dict]]) -> str:
        context_blocks = []
        for query, results in retrieval_results.items():
            context_blocks.append(f"## Query: {query}\n")
            for i, result in enumerate(results, 1):
                metadata = result["metadata"]
                source = metadata.get("source", "Unknown")
                context_blocks.append(
                    f"[{i}] Source: {source}\n{result['text']}\n"
                )
        return "\n".join(context_blocks)
