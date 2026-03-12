from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict
from .embeddings import EmbeddingService
import uuid

class VectorStore:
    def __init__(self, host: str, port: int, collection_name: str, embedding_model: str):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.embeddings = EmbeddingService(embedding_model)
        self._ensure_collection()
    
    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
            )
    
    def add_documents(self, chunks: List[Dict]):
        texts = [c["text"] for c in chunks]
        vectors = self.embeddings.embed_documents(texts)
        
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk["text"],
                    "metadata": chunk["metadata"]
                }
            )
            for chunk, vector in zip(chunks, vectors)
        ]
        
        self.client.upsert(collection_name=self.collection_name, points=points)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_vector = self.embeddings.embed_text(query)
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        return [
            {
                "text": r.payload["text"],
                "metadata": r.payload["metadata"],
                "score": r.score
            }
            for r in results
        ]
