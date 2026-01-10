from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import summary, decision
from app.database import init_supabase


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        from app.database import SUPABASE_AVAILABLE
        if SUPABASE_AVAILABLE and settings.supabase_key:
            if init_supabase():
                print("✅ Supabase povezava uspešna")
            else:
                print("⚠️ Supabase povezava ni uspela - aplikacija bo delovala brez shranjevanja")
        elif not SUPABASE_AVAILABLE:
            print("⚠️ Supabase paket ni nameščen - aplikacija bo delovala brez shranjevanja")
        else:
            print("⚠️ Supabase key ni nastavljen - aplikacija bo delovala brez shranjevanja")
    except Exception as e:
        print(f"⚠️ Napaka pri inicializaciji Supabase: {e}")
    
    yield
    
    # Shutdown (če je potrebno)


app = FastAPI(
    title="AI Summary API",
    description="Backend API for AI Summary application - Generator povzetkov z LLM modeli",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(summary.router)
app.include_router(decision.router)

@app.get("/")
def read_root():
    """Root endpoint - osnovne informacije o API-ju"""
    from app.database import SUPABASE_AVAILABLE
    
    db_status = "Not configured"
    if SUPABASE_AVAILABLE and settings.supabase_key:
        db_status = "Supabase (configured)"
    elif SUPABASE_AVAILABLE:
        db_status = "Supabase (key missing)"
    elif not SUPABASE_AVAILABLE:
        db_status = "Supabase (package not installed)"
    
    return {
        "message": "AI Summary API - Generator povzetkov z LLM modeli",
        "status": "running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "database": {
            "type": "Supabase",
            "status": db_status,
            "url": settings.supabase_url if settings.supabase_key else None
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint - preveri stanje aplikacije in Supabase"""
    from app.database import SUPABASE_AVAILABLE, init_supabase
    
    health_status = {
        "status": "healthy",
        "database": {
            "supabase_available": SUPABASE_AVAILABLE,
            "supabase_connected": False,
            "supabase_key_set": bool(settings.supabase_key)
        }
    }
    
    if SUPABASE_AVAILABLE and settings.supabase_key:
        try:
            health_status["database"]["supabase_connected"] = init_supabase()
        except Exception as e:
            health_status["database"]["error"] = str(e)
    
    return health_status


@app.get("/database/status")
def database_status():
    """Preveri stanje Supabase baze podatkov"""
    from app.database import SUPABASE_AVAILABLE, get_supabase
    
    status = {
        "supabase_available": SUPABASE_AVAILABLE,
        "supabase_key_set": bool(settings.supabase_key),
        "supabase_url": settings.supabase_url,
        "tables": []
    }
    
    if SUPABASE_AVAILABLE and settings.supabase_key:
        try:
            supabase = get_supabase()
            
            # Preveri tabele - samo uporabljene
            tables_to_check = [
                "summaries",
                "model_comparisons",
                "comparison_results"
            ]
            
            for table_name in tables_to_check:
                try:
                    result = supabase.table(table_name).select("id").limit(1).execute()
                    status["tables"].append({
                        "name": table_name,
                        "accessible": True,
                        "row_count": len(result.data) if result.data else 0
                    })
                except Exception as e:
                    status["tables"].append({
                        "name": table_name,
                        "accessible": False,
                        "error": str(e)
                    })
            
            status["connection_status"] = "connected"
        except Exception as e:
            status["connection_status"] = "error"
            status["error"] = str(e)
    else:
        status["connection_status"] = "not_configured"
        if not SUPABASE_AVAILABLE:
            status["error"] = "Supabase paket ni nameščen"
        elif not settings.supabase_key:
            status["error"] = "Supabase key ni nastavljen"
    
    return status