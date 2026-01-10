"""
Service za delo z Supabase bazo podatkov
"""
from typing import Optional
from app.database import get_supabase, SUPABASE_AVAILABLE
from app.models.database import (
    SummaryRecord,
    ModelComparisonRecord,
    ComparisonAnalysis
)
from app.schemas.summary import SummaryResponse, ComparisonResponse


class DatabaseService:
    """Service za shranjevanje in pridobivanje podatkov iz Supabase"""
    
    @staticmethod
    async def save_summary(summary_response: SummaryResponse, original_text: str) -> Optional[SummaryRecord]:
        """Shrani povzetek v bazo"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase()
            
            # Določi provider iz modela
            provider = "OpenAI"
            model_lower = summary_response.model.lower()
            if "claude" in model_lower or "anthropic" in model_lower:
                provider = "Anthropic"
            elif "gpt" in model_lower or "openai" in model_lower:
                provider = "OpenAI"
            
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
        except Exception as e:
            print(f"Napaka pri shranjevanju povzetka v bazo: {e}")
            return None
    
    @staticmethod
    async def save_comparison(comparison_response: ComparisonResponse, original_text: str) -> Optional[ModelComparisonRecord]:
        """Shrani primerjavo modelov v bazo in podrobne rezultate za vsak model"""
        if not SUPABASE_AVAILABLE:
            return None
        
        try:
            supabase = get_supabase()
            
            # 1. Shrani glavno primerjavo
            # Serializiraj rezultate - pretvori datetime v string
            results_data = []
            for r in comparison_response.results:
                try:
                    result_dict = r.model_dump() if hasattr(r, 'model_dump') else r.dict()
                    # Pretvori datetime v ISO format string
                    if "metrics" in result_dict and isinstance(result_dict["metrics"], dict):
                        if "timestamp" in result_dict["metrics"]:
                            timestamp = result_dict["metrics"]["timestamp"]
                            if hasattr(timestamp, "isoformat"):
                                result_dict["metrics"]["timestamp"] = timestamp.isoformat()
                            elif isinstance(timestamp, str):
                                pass  # Already a string
                    results_data.append(result_dict)
                except Exception as serialize_error:
                    print(f"Napaka pri serializaciji rezultata: {serialize_error}")
                    # Poskusi z osnovno serializacijo
                    try:
                        results_data.append({
                            "model": r.model,
                            "summary": r.summary,
                            "metrics": {
                                "response_time_ms": r.metrics.response_time_ms,
                                "tokens_used": r.metrics.tokens_used,
                                "cost_usd": r.metrics.cost_usd
                            }
                        })
                    except:
                        pass
            
            # Serializiraj comparison
            comparison_dict = comparison_response.comparison.model_dump() if hasattr(comparison_response.comparison, 'model_dump') else comparison_response.comparison.dict()
            
            # Odstrani prefiks iz modelnih imen za shranjevanje (openai/ ali anthropic/)
            fastest_model = comparison_response.comparison.fastest.replace("openai/", "").replace("anthropic/", "")
            cheapest_model = comparison_response.comparison.cheapest.replace("openai/", "").replace("anthropic/", "")
            
            comparison_data = {
                "original_text": original_text,
                "comparison_data": {
                    "results": results_data,
                    "comparison": comparison_dict
                },
                "fastest_model": fastest_model,
                "cheapest_model": cheapest_model,
                "average_response_time": comparison_response.comparison.average_response_time,
                "total_cost": comparison_response.comparison.total_cost
            }
            
            comparison_result = supabase.table("model_comparisons").insert(comparison_data).execute()
            comparison_record = ModelComparisonRecord(**comparison_result.data[0])
            comparison_id = comparison_record.id
            
            # 2. Shrani podrobne rezultate za vsak model
            for result in comparison_response.results:
                try:
                    # Določi provider
                    provider = "OpenAI"
                    model_lower = result.model.lower()
                    if "claude" in model_lower or "anthropic" in model_lower:
                        provider = "Anthropic"
                    elif "gpt" in model_lower or "openai" in model_lower:
                        provider = "OpenAI"
                    
                    result_data = {
                        "comparison_id": str(comparison_id),
                        "model_name": result.model.replace("openai/", "").replace("anthropic/", ""),
                        "provider": provider,
                        "summary_text": result.summary,
                        "response_time_ms": result.metrics.response_time_ms,
                        "tokens_used": result.metrics.tokens_used,
                        "cost_usd": result.metrics.cost_usd,
                        "summary_length": len(result.summary) if result.summary else 0
                    }
                    
                    supabase.table("comparison_results").insert(result_data).execute()
                except Exception as result_error:
                    print(f"Napaka pri shranjevanju rezultata za model {result.model}: {result_error}")
                    # Nadaljujemo z naslednjim modelom
            
            return comparison_record
        except ValueError as ve:
            # Supabase ni nameščen ali ni ključa
            print(f"Supabase ni na voljo: {ve}")
            return None
        except Exception as e:
            print(f"Napaka pri shranjevanju primerjave v bazo: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    async def get_comparison_analysis() -> list[ComparisonAnalysis]:
        """Pridobi analizo primerjav - agregirane statistike"""
        if not SUPABASE_AVAILABLE:
            return []
        
        try:
            supabase = get_supabase()
            
            result = supabase.table("comparison_analysis").select("*").execute()
            return [ComparisonAnalysis(**row) for row in result.data]
        except Exception as e:
            print(f"Napaka pri pridobivanju analize primerjav: {e}")
            return []
