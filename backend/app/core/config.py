from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "LegalBot API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/legalbot"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # PROVEEDOR DE LLM (Elige uno)
    
    # Opciones: "auto", "groq", "gemini", "ollama", "openai", "together"
    LLM_PROVIDER: str = "auto"  # auto detecta según API keys disponibles
    
    # OpenAI 
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # Groq 
    GROQ_API_KEY: str = ""
    
    # Google Gemini 
    GOOGLE_API_KEY: str = ""
    
    # Together AI 
    TOGETHER_API_KEY: str = ""
    
    # Ollama (100% local y gratis)
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1"
    
   
    # PINECONE (Vector Database) - O usar embeddings locales
    
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = "us-east-1"
    PINECONE_INDEX_NAME: str = "legalbot-laws"
    
    # Embeddings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Culqi (Payments)
    CULQI_PUBLIC_KEY: str = ""
    CULQI_PRIVATE_KEY: str = ""
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "https://legalbot.pe"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  #  - Ignora variables extra del .env


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()