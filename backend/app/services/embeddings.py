from langchain_openai import OpenAIEmbeddings
from typing import List

class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.embeddings = OpenAIEmbeddings(model=model)
    
    def embed_text(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
