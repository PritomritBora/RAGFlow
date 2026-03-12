from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List

class EmbeddingService:
    def __init__(self, model: str = "text-embedding-3-small", provider: str = "openai", api_key: str = None):
        self.provider = provider
        if provider == "gemini":
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=model,
                google_api_key=api_key
            )
        else:  # openai
            self.embeddings = OpenAIEmbeddings(model=model, openai_api_key=api_key)
    
    def embed_text(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(texts)
