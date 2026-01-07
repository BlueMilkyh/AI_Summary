"""
API router za povzetke
"""
from fastapi import APIRouter, HTTPException
from app.schemas.summary import (
    SummaryRequest, 
    SummaryResponse, 
    ComparisonRequest, 
    ComparisonResponse
)
from app.config import settings
from app.services.google_service import GoogleService
# TODO: Dodaj ostale servise ko bodo implementirani
# from app.services.openai_service import OpenAIService
# from app.services.anthropic_service import AnthropicService

router = APIRouter(prefix="/api/summary", tags=["summary"])


def get_service_for_model(model: str):
    """
    Vrne ustrezen LLM service za dani model
    """
    model_lower = model.lower()
    
    if "gemini" in model_lower or "google" in model_lower:
        if not settings.google_api_key:
            raise HTTPException(
                status_code=400, 
                detail="Google API key ni nastavljen. Dodajte GOOGLE_API_KEY v .env datoteko."
            )
        return GoogleService(model_name=model if "gemini" in model_lower else "gemini-pro", 
                            api_key=settings.google_api_key)
    
    # TODO: Dodaj ostale modele
    # elif "gpt" in model_lower or "openai" in model_lower:
    #     return OpenAIService(...)
    # elif "claude" in model_lower or "anthropic" in model_lower:
    #     return AnthropicService(...)
    
    raise HTTPException(
        status_code=400, 
        detail=f"Model '{model}' ni podprt. Podprti modeli: gemini-pro, gemini-1.5-pro"
    )


@router.post("/generate", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest):
    """
    Generira povzetek z izbranim LLM modelom
    """
    try:
        service = get_service_for_model(request.model)
        result = await service.generate_summary(request.text, request.max_length)
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
        
        return ComparisonResponse(
            results=results,
            comparison=comparison
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Napaka pri primerjavi modelov: {str(e)}"
        )


@router.get("/models")
async def list_models():
    """
    Vrne seznam vseh podprtih modelov
    """
    models = []
    
    # Google Gemini modeli
    if settings.google_api_key:
        try:
            google_service = GoogleService(api_key=settings.google_api_key)
            google_info = google_service.get_model_info()
            models.append({
                **google_info,
                "status": "available"
            })
            # Dodaj tudi Gemini 1.5 Pro če je podprt
            models.append({
                "id": "gemini-1.5-pro",
                "name": "Gemini 1.5 Pro",
                "provider": "Google",
                "supports_streaming": False,
                "max_tokens": 32768,
                "status": "available"
            })
        except:
            pass
    
    # TODO: Dodaj ostale modele ko bodo implementirani
    # if settings.openai_api_key:
    #     models.append({...})
    
    return {"models": models}

