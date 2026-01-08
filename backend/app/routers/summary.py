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
from app.services.openai_service import OpenAIService
from app.services.anthropic_service import AnthropicService

router = APIRouter(prefix="/api/summary", tags=["summary"])


def get_service_for_model(model: str):
    """
    Vrne ustrezen LLM service za dani model
    Podprti modeli: 
    - Google: gemini-2.5-flash, gemini-2.5-pro, gemini-2.0-flash
    - OpenAI: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
    - Anthropic: claude-3-5-sonnet-20241022, claude-3-5-haiku-20241022, claude-3-opus-20240229
    """
    model_lower = model.lower()
    
    # Dovoljeni Google modeli
    allowed_google_models = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"]
    # Dovoljeni OpenAI modeli
    allowed_openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
    # Dovoljeni Anthropic modeli
    allowed_anthropic_models = ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"]
    
    if "gemini" in model_lower or "google" in model_lower:
        if not settings.google_api_key:
            raise HTTPException(
                status_code=400, 
                detail="Google API key ni nastavljen. Dodajte GOOGLE_API_KEY v .env datoteko."
            )
        
        # Preveri, če je model med dovoljenimi
        if model in allowed_google_models:
            return GoogleService(model_name=model, api_key=settings.google_api_key)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{model}' ni podprt. Podprti Google modeli: {', '.join(allowed_google_models)}"
            )
    
    elif "gpt" in model_lower or "openai" in model_lower:
        # Odstrani OpenRouter prefiks če je prisoten (openai/model-name -> model-name)
        clean_model = model.replace("openai/", "") if model.startswith("openai/") else model
        
        # Preveri ali uporabljamo OpenRouter
        if settings.use_openrouter:
            if not settings.openrouter_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="OpenRouter API key ni nastavljen. Dodajte OPENROUTER_API_KEY v .env datoteko."
                )
        else:
            if not settings.openai_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="OpenAI API key ni nastavljen. Dodajte OPENAI_API_KEY v .env datoteko."
                )
        
        # Preveri, če je model (brez prefiksa) med dovoljenimi
        if clean_model in allowed_openai_models:
            return OpenAIService(model_name=clean_model, api_key=settings.openai_api_key)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{clean_model}' ni podprt. Podprti OpenAI modeli: {', '.join(allowed_openai_models)}"
            )
    
    elif "claude" in model_lower or "anthropic" in model_lower:
        # Odstrani OpenRouter prefiks če je prisoten (anthropic/model-name -> model-name)
        clean_model = model.replace("anthropic/", "") if model.startswith("anthropic/") else model
        
        # Preveri ali uporabljamo OpenRouter
        if settings.use_openrouter:
            if not settings.openrouter_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="OpenRouter API key ni nastavljen. Dodajte OPENROUTER_API_KEY v .env datoteko."
                )
        else:
            if not settings.anthropic_api_key:
                raise HTTPException(
                    status_code=400,
                    detail="Anthropic API key ni nastavljen. Dodajte ANTHROPIC_API_KEY v .env datoteko."
                )
        
        # Preveri, če je model (brez prefiksa) med dovoljenimi
        if clean_model in allowed_anthropic_models:
            return AnthropicService(model_name=clean_model, api_key=settings.anthropic_api_key)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Model '{clean_model}' ni podprt. Podprti Anthropic modeli: {', '.join(allowed_anthropic_models)}"
            )
    
    all_allowed = allowed_google_models + allowed_openai_models + allowed_anthropic_models
    raise HTTPException(
        status_code=400, 
        detail=f"Model '{model}' ni podprt. Podprti modeli: {', '.join(all_allowed)}"
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
    
    # Google Gemini modeli - samo 3 izbrani modeli
    if settings.google_api_key:
        # Dodaj samo 3 zahtevane modele
        models.extend([
            {
                "id": "gemini-2.5-flash",
                "name": "Gemini 2.5 Flash",
                "provider": "Google",
                "supports_streaming": False,
                "max_tokens": 1048576,
                "status": "available"
            },
            {
                "id": "gemini-2.5-pro",
                "name": "Gemini 2.5 Pro",
                "provider": "Google",
                "supports_streaming": False,
                "max_tokens": 2097152,
                "status": "available"
            },
            {
                "id": "gemini-2.0-flash",
                "name": "Gemini 2.0 Flash",
                "provider": "Google",
                "supports_streaming": False,
                "max_tokens": 1048576,
                "status": "available"
            }
        ])
    
    # OpenAI modeli - 3 izbrani modeli
    if settings.openai_api_key:
        try:
            # Ustvari servise za pridobitev informacij
            gpt4o_mini = OpenAIService(model_name="gpt-4o-mini", api_key=settings.openai_api_key)
            gpt4o = OpenAIService(model_name="gpt-4o", api_key=settings.openai_api_key)
            gpt35 = OpenAIService(model_name="gpt-3.5-turbo", api_key=settings.openai_api_key)
            
            models.extend([
                {
                    **gpt4o_mini.get_model_info(),
                    "status": "available"
                },
                {
                    **gpt4o.get_model_info(),
                    "status": "available"
                },
                {
                    **gpt35.get_model_info(),
                    "status": "available"
                }
            ])
        except Exception as e:
            # Če pride do napake, dodaj osnovne informacije
            models.extend([
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
                    "id": "gpt-3.5-turbo",
                    "name": "GPT-3.5 Turbo",
                    "provider": "OpenAI",
                    "supports_streaming": True,
                    "max_tokens": 16385,
                    "status": "available"
                }
            ])
    
    # Anthropic Claude modeli - 3 izbrani modeli
    if settings.anthropic_api_key:
        try:
            # Ustvari servise za pridobitev informacij
            claude35_sonnet = AnthropicService(model_name="claude-3-5-sonnet-20241022", api_key=settings.anthropic_api_key)
            claude35_haiku = AnthropicService(model_name="claude-3-5-haiku-20241022", api_key=settings.anthropic_api_key)
            claude3_opus = AnthropicService(model_name="claude-3-opus-20240229", api_key=settings.anthropic_api_key)
            
            models.extend([
                {
                    **claude35_sonnet.get_model_info(),
                    "status": "available"
                },
                {
                    **claude35_haiku.get_model_info(),
                    "status": "available"
                },
                {
                    **claude3_opus.get_model_info(),
                    "status": "available"
                }
            ])
        except Exception as e:
            # Če pride do napake, dodaj osnovne informacije
            models.extend([
                {
                    "id": "claude-3-5-sonnet-20241022",
                    "name": "Claude 3.5 Sonnet",
                    "provider": "Anthropic",
                    "supports_streaming": True,
                    "max_tokens": 200000,
                    "status": "available"
                },
                {
                    "id": "claude-3-5-haiku-20241022",
                    "name": "Claude 3.5 Haiku",
                    "provider": "Anthropic",
                    "supports_streaming": True,
                    "max_tokens": 200000,
                    "status": "available"
                },
                {
                    "id": "claude-3-opus-20240229",
                    "name": "Claude 3 Opus",
                    "provider": "Anthropic",
                    "supports_streaming": True,
                    "max_tokens": 200000,
                    "status": "available"
                }
            ])
    
    return {"models": models}

