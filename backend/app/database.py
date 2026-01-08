"""
Supabase database connection and utilities
"""
from supabase import create_client, Client
from app.config import settings
from typing import Optional

# Global Supabase client
_supabase: Optional[Client] = None


def get_supabase() -> Client:
    """Vrne Supabase client (singleton pattern)"""
    global _supabase
    if _supabase is None:
        if not settings.supabase_key:
            raise ValueError("Supabase key ni nastavljen. Dodajte SUPABASE_KEY v .env datoteko.")
        _supabase = create_client(settings.supabase_url, settings.supabase_key)
    return _supabase


def init_supabase():
    """Inicializira Supabase povezavo"""
    try:
        client = get_supabase()
        # Test povezave
        client.table("summaries").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Napaka pri inicializaciji Supabase: {e}")
        return False
