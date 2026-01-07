from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import summary

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

@app.get("/")
def read_root():
    return {
        "message": "AI Summary API - Generator povzetkov z LLM modeli",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}