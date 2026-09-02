from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    #API Keys
    google_api_key:str

    # Models
    embedding_model: str = "all-MiniLM-L6-v2"
    llm_model: str = "gemini-2.5-flash"

    # Storage
    chroma_path: str = "backend/storage/chroma"
    upload_path: str = "backend/storage/uploads"

    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT / ".env",
        extra="ignore",
    )

settings = Settings()