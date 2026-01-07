"""
Konfiguracija aplikacije - API ključi in nastavitve
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # LLM API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = "AIzaSyAAhFfK3YqLm7F2lQ2HA4RCVfXBIfDAa_s"  # Default value, override with .env
    huggingface_api_key: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

