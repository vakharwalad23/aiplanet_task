from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PDF QA System"
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./pdf_docs.db"
    
    # MinIO Settings
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "pdfdocs"
    MINIO_SECURE: bool = False
    
    # Langchain Settings
    LANGCHAIN_TRACING_V2: str = 'true'
    LANGCHAIN_ENDPOINT: str = 'https://api.smith.langchain.com'
    LANGCHAIN_API_KEY: str = 'LANGCHAIN_API_KEY'
    LANGCHAIN_PROJECT: str = 'PDF_QA'

    # OpenAI Settings
    OPENAI_API_KEY: str = ""

    # GROQ Settings
    GROQ_API_KEY: str = ""
    
    # File Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()