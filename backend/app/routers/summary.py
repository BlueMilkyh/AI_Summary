"""
API router za povzetke - samo OpenRouter API z 3 modeli
"""
from fastapi import APIRouter, HTTPException
from app.schemas.summary import (
    SummaryRequest, 
    SummaryResponse, 
    ComparisonRequest, 
    ComparisonResponse
)
from app.config import settings
from app.services.openai_service import OpenAIService
from app.services.anthropic_service import AnthropicService
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/api/summary", tags=["summary"])

# Dovoljeni modeli - samo 3
ALLOWED_MODELS = {
    "gpt-4o-mini": {"provider": "OpenAI", "service": "openai"},
    "gpt-4o": {"provider": "OpenAI", "service": "openai"},
    "claude-3-5-sonnet-20241022": {"provider": "Anthropic", "service": "anthropic"}
}


def get_service_for_model(model: str):
    """
    Vrne ustrezen LLM service za dani model - samo OpenRouter
    Podprti modeli: 
    - OpenAI: gpt-4o-mini, gpt-4o
    - Anthropic: claude-3-5-sonnet-20241022
    """
    if not settings.openrouter_api_key:
        raise HTTPException(
            status_code=400,
            detail="OpenRouter API key ni nastavljen. Dodajte OPENROUTER_API_KEY v .env datoteko."
        )
    
    # Odstrani prefiks če je prisoten (openai/model-name ali anthropic/model-name)
    clean_model = model.replace("openai/", "").replace("anthropic/", "")
    
    if clean_model not in ALLOWED_MODELS:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model}' ni podprt. Podprti modeli: {', '.join(ALLOWED_MODELS.keys())}"
        )
    
    model_info = ALLOWED_MODELS[clean_model]
    
    if model_info["service"] == "openai":
        return OpenAIService(model_name=clean_model, api_key=settings.openrouter_api_key)
    elif model_info["service"] == "anthropic":
        return AnthropicService(model_name=clean_model, api_key=settings.openrouter_api_key)
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Neznan tip servisa za model '{clean_model}'"
        )


@router.post("/generate", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generira povzetek z izbranim LLM modelom in ga shrani v bazo
    """
    try:
        service = get_service_for_model(request.model)
        result = await service.generate_summary(request.text, request.max_length)
        
        # Shrani v Supabase
        try:
            await DatabaseService.save_summary(result, request.text)
        except Exception as db_error:
            print(f"Napaka pri shranjevanju v bazo: {db_error}")
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Napaka pri generiranju povzetka: {str(e)}")


@router.post("/compare", response_model=ComparisonResponse)
async def compare_models(request: ComparisonRequest):
    """
    Generira povzetke z več modeli hkrati in jih primerja
    """
    import asyncio
    from app.utils.metrics import calculate_comparison
    
    # Generiraj povzetke za vse modele paralelno
    tasks = []
    for model in request.models:
        try:
            service = get_service_for_model(model)
            task = service.generate_summary(request.text, request.max_length)
            tasks.append(task)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Napaka pri inicializaciji modela '{model}': {str(e)}"
            )
    
    try:
        # Počakaj na vse rezultate
        results = await asyncio.gather(*tasks)
        
        # Izračunaj primerjavo
        comparison = calculate_comparison(results)
        
        comparison_response = ComparisonResponse(
            results=results,
            comparison=comparison
        )
        
        # Shrani primerjavo v Supabase
        try:
            await DatabaseService.save_comparison(comparison_response, request.text)
        except Exception as db_error:
            print(f"Napaka pri shranjevanju primerjave v bazo: {db_error}")
        
        return comparison_response
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Napaka pri primerjavi modelov: {str(e)}"
        )


@router.get("/models")
async def list_models():
    """
    Vrne seznam podprtih modelov - samo 3 modeli preko OpenRouter
    """
    if not settings.openrouter_api_key:
        return {
            "models": [],
            "error": "OpenRouter API key ni nastavljen"
        }
    
    models = [
        {
            "id": "gpt-4o-mini",
            "name": "GPT-4o Mini",
            "provider": "OpenAI",
            "supports_streaming": True,
            "max_tokens": 128000,
            "status": "available"
        },
        {
            "id": "gpt-4o",
            "name": "GPT-4o",
            "provider": "OpenAI",
            "supports_streaming": True,
            "max_tokens": 128000,
            "status": "available"
        },
        {
            "id": "claude-3-5-sonnet-20241022",
            "name": "Claude 3.5 Sonnet",
            "provider": "Anthropic",
            "supports_streaming": True,
            "max_tokens": 200000,
            "status": "available"
        }
    ]
    
    return {"models": models}
