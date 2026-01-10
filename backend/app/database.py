"""
Supabase database connection and utilities
"""
from app.config import settings
from typing import Optional

# Global Supabase client
_supabase = None

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    # Supabase paket ni nameščen - shranjevanje bo onemogočeno


def get_supabase():
    """Vrne Supabase client (singleton pattern)"""
    global _supabase
    
    if not SUPABASE_AVAILABLE:
        raise ValueError("Supabase paket ni nameščen. Namestite z: pip install supabase")
    
    if _supabase is None:
        if not settings.supabase_key:
            raise ValueError("Supabase key ni nastavljen. Dodajte SUPABASE_KEY v .env datoteko.")
        _supabase = create_client(settings.supabase_url, settings.supabase_key)
    return _supabase


def init_supabase():
    """Inicializira Supabase povezavo"""
    if not SUPABASE_AVAILABLE:
        return False
    
    try:
        client = get_supabase()
        # Test povezave - poskusi pridobiti podatke iz tabele
        client.table("summaries").select("id").limit(1).execute()
        return True
    except Exception as e:
        print(f"Napaka pri inicializaciji Supabase: {e}")
        return False
