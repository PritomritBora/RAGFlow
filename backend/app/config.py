from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Provider: 'openai' or 'gemini'
    llm_provider: str = "gemini"
    
    # OpenAI settings (if using OpenAI)
    openai_api_key: str = ""
    
    # Google Gemini settings (if using Gemini)
    google_api_key: str = ""
    
    # Model settings
    llm_model: str = "gemini-1.5-flash"  # or gemini-1.5-pro for better quality
    embedding_model: str = "models/embedding-001"
    
    # Qdrant settings
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "research_docs"
    
    class Config:
        env_file = ".env"

settings = Settings()
