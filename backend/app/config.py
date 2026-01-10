"""
Konfiguracija aplikacije - API ključi in nastavitve
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # OpenRouter API Key (samo OpenRouter)
    openrouter_api_key: str = "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"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    
    # Supabase settings
    supabase_url: str = "https://qrzbldfflvfuqhwgcgvq.supabase.co"
    supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFyemJsZGZmbHZmdXFod2djZ3ZxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njc4NzEzODcsImV4cCI6MjA4MzQ0NzM4N30.qxDJDc8R5rHADn8TG8LKIiSZFPgGJR8pUUkdM9wE36I"  # Anon key
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

