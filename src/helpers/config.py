from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

# Get the absolute path to the src directory where .env is located
SRC_DIR = Path(__file__).parent.parent
ENV_FILE = SRC_DIR / ".env"

class Settings(BaseSettings):
    
    APP_NAME: str
    APP_VERSION: str
    GROQ_API_KEY: str
    
    
    GROQ_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    
    FILE_DEFAULT_CHUNK_SIZE: int
    
    MONGODB_URL: str
    MONGODB_DATABASE: str
    
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore"
    )
        
@lru_cache()
def get_settings():
    return Settings()