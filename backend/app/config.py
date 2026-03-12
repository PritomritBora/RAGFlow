from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    llm_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "research_docs"
    
    class Config:
        env_file = ".env"

settings = Settings()
