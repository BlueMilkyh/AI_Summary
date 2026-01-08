from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import summary, decision
from app.database import init_supabase

app = FastAPI(
    title="AI Summary API",
    description="Backend API for AI Summary application - Generator povzetkov z LLM modeli",
    version="1.0.0"
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

# Inicializiraj Supabase
@app.on_event("startup")
async def startup_event():
    if settings.supabase_key:
        if init_supabase():
            print("✅ Supabase povezava uspešna")
        else:
            print("⚠️ Supabase povezava ni uspela - aplikacija bo delovala brez shranjevanja")
    else:
        print("⚠️ Supabase key ni nastavljen - aplikacija bo delovala brez shranjevanja")

@app.get("/")
def read_root():
    return {
        "message": "AI Summary API - Generator povzetkov z LLM modeli",
        "status": "running",
        "docs": "/docs",
        "database": "Supabase" if settings.supabase_key else "Not configured"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}