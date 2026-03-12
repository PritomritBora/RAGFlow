from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import uuid

class VectorStore:
    def __init__(self, host: str, port: int, collection_name: str, embedding_model: str):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name
        self.embedder = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedder.get_sentence_embedding_dimension()
        self._ensure_collection()
    
    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if not any(c.name == self.collection_name for c in collections):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.embedding_dim, distance=Distance.COSINE)
            )
    
    def add_documents(self, documents: List[Dict]):
        points = []
        for doc in documents:
            embedding = self.embedder.encode(doc["text"]).tolist()
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": doc["text"],
                    "metadata": doc.get("metadata", {})
                }
            ))
        self.client.upsert(collection_name=self.collection_name, points=points)
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_vector = self.embedder.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        return [
            {
                "text": hit.payload["text"],
                "metadata": hit.payload["metadata"],
                "score": hit.score
            }
            for hit in results
        ]
