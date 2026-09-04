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
    database_url: str = "sqlite:///./backend/storage/app.db"

    #Auth
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(
        env_file= PROJECT_ROOT / ".env",
        extra="ignore",
    )

settings = Settings()