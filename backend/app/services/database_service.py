"""
Service za delo z Supabase bazo podatkov
"""
from typing import List, Optional, Dict, Any
from app.database import get_supabase
from app.models.database import (
    SummaryRecord,
    ModelComparisonRecord,
    UserRatingRecord,
    ModelStatistics
)
from app.schemas.summary import SummaryResponse, ComparisonResponse
from uuid import UUID


class DatabaseService:
    """Service za shranjevanje in pridobivanje podatkov iz Supabase"""
    
    @staticmethod
    async def save_summary(summary_response: SummaryResponse, original_text: str) -> SummaryRecord:
        """Shrani povzetek v bazo"""
        supabase = get_supabase()
        
        # Določi provider iz modela
        provider = "Google"
        if "gpt" in summary_response.model.lower() or "openai" in summary_response.model.lower():
            provider = "OpenAI"
        elif "claude" in summary_response.model.lower() or "anthropic" in summary_response.model.lower():
            provider = "Anthropic"
        
        data = {
            "original_text": original_text,
            "summary_text": summary_response.summary,
            "model_name": summary_response.model.replace("openai/", "").replace("anthropic/", ""),
            "provider": provider,
            "response_time_ms": summary_response.metrics.response_time_ms,
            "tokens_used": summary_response.metrics.tokens_used,
            "cost_usd": summary_response.metrics.cost_usd,
        }
        
        result = supabase.table("summaries").insert(data).execute()
        return SummaryRecord(**result.data[0])
    
    @staticmethod
    async def save_comparison(comparison_response: ComparisonResponse, original_text: str) -> ModelComparisonRecord:
        """Shrani primerjavo modelov v bazo"""
        supabase = get_supabase()
        
        data = {
            "original_text": original_text,
            "comparison_data": {
                "results": [r.dict() for r in comparison_response.results],
                "comparison": comparison_response.comparison.dict()
            },
            "fastest_model": comparison_response.comparison.fastest,
            "cheapest_model": comparison_response.comparison.cheapest,
            "average_response_time": comparison_response.comparison.average_response_time,
            "total_cost": comparison_response.comparison.total_cost
        }
        
        result = supabase.table("model_comparisons").insert(data).execute()
        return ModelComparisonRecord(**result.data[0])
    
    @staticmethod
    async def save_rating(summary_id: UUID, model_name: str, rating: int, feedback: Optional[str] = None) -> UserRatingRecord:
        """Shrani uporabniško oceno"""
        supabase = get_supabase()
        
        data = {
            "summary_id": str(summary_id),
            "model_name": model_name,
            "rating": rating,
            "feedback": feedback
        }
        
        result = supabase.table("user_ratings").insert(data).execute()
        return UserRatingRecord(**result.data[0])
    
    @staticmethod
    async def get_model_statistics(model_name: Optional[str] = None) -> List[ModelStatistics]:
        """Pridobi statistike za modele"""
        supabase = get_supabase()
        
        query = supabase.table("model_statistics").select("*")
        
        if model_name:
            query = query.eq("model_name", model_name)
        
        result = query.execute()
        return [ModelStatistics(**row) for row in result.data]
    
    @staticmethod
    async def get_best_models_by_criteria() -> Dict[str, Dict[str, Any]]:
        """Pridobi najboljše modele po različnih kriterijih"""
        supabase = get_supabase()
        
        result = supabase.table("best_models_by_criteria").select("*").execute()
        
        best_models = {}
        for row in result.data:
            criterion = row["criterion"]
            best_models[criterion] = {
                "model_name": row["model_name"],
                "provider": row["provider"],
                "value": row["value"]
            }
        
        return best_models
    
    @staticmethod
    async def get_recent_summaries(limit: int = 10) -> List[SummaryRecord]:
        """Pridobi zadnje povzetke"""
        supabase = get_supabase()
        
        result = supabase.table("summaries").select("*").order("created_at", desc=True).limit(limit).execute()
        return [SummaryRecord(**row) for row in result.data]
