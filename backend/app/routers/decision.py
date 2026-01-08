"""
API router za odločanje (decision making) na podlagi podatkov
"""
from fastapi import APIRouter, HTTPException
from typing import Optional, List, Dict, Any
from app.services.database_service import DatabaseService
from app.models.database import ModelStatistics

router = APIRouter(prefix="/api/decision", tags=["decision"])


@router.get("/recommend")
async def recommend_model(
    criteria: str = "balanced",  # balanced, speed, cost, quality
    text_length: Optional[int] = None
):
    """
    Priporoči najboljši model na podlagi kriterijev in zgodovinskih podatkov
    
    Kriteriji:
    - balanced: Uravnotežena izbira (hitrost + cena + kvaliteta)
    - speed: Najhitrejši model
    - cost: Najcenejši model
    - quality: Najbolj ocenjen model
    """
    try:
        stats = await DatabaseService.get_model_statistics()
        best_models = await DatabaseService.get_best_models_by_criteria()
        
        if not stats:
            raise HTTPException(
                status_code=404,
                detail="Ni podatkov za odločanje. Najprej generirajte nekaj povzetkov."
            )
        
        if criteria == "speed":
            # Najhitrejši model
            fastest = min(stats, key=lambda s: s.avg_response_time_ms)
            return {
                "recommended_model": fastest.model_name,
                "provider": fastest.provider,
                "reason": "Najhitrejši model glede na povprečen čas odziva",
                "metrics": {
                    "avg_response_time_ms": fastest.avg_response_time_ms,
                    "total_summaries": fastest.total_summaries
                }
            }
        
        elif criteria == "cost":
            # Najcenejši model
            cheapest = min(stats, key=lambda s: s.avg_cost_usd)
            return {
                "recommended_model": cheapest.model_name,
                "provider": cheapest.provider,
                "reason": "Najcenejši model glede na povprečne stroške",
                "metrics": {
                    "avg_cost_usd": cheapest.avg_cost_usd,
                    "total_summaries": cheapest.total_summaries
                }
            }
        
        elif criteria == "quality":
            # Najbolj ocenjen model
            rated_models = [s for s in stats if s.avg_rating and s.avg_rating > 0]
            if not rated_models:
                raise HTTPException(
                    status_code=404,
                    detail="Ni ocen za modele. Najprej ocenite nekaj povzetkov."
                )
            best_rated = max(rated_models, key=lambda s: s.avg_rating)
            return {
                "recommended_model": best_rated.model_name,
                "provider": best_rated.provider,
                "reason": "Najbolj ocenjen model glede na uporabniške ocene",
                "metrics": {
                    "avg_rating": best_rated.avg_rating,
                    "total_ratings": best_rated.total_ratings,
                    "total_summaries": best_rated.total_summaries
                }
            }
        
        else:  # balanced
            # Uravnotežena izbira - kombinacija vseh kriterijev
            scored_models = []
            for stat in stats:
                if stat.total_summaries == 0:
                    continue
                
                # Normaliziraj vrednosti (0-1)
                max_time = max(s.avg_response_time_ms for s in stats)
                max_cost = max(s.avg_cost_usd for s in stats)
                max_rating = max((s.avg_rating or 0) for s in stats) or 1
                
                speed_score = 1 - (stat.avg_response_time_ms / max_time) if max_time > 0 else 0
                cost_score = 1 - (stat.avg_cost_usd / max_cost) if max_cost > 0 else 0
                quality_score = (stat.avg_rating or 0) / max_rating if max_rating > 0 else 0
                
                # Uteži: 40% hitrost, 30% cena, 30% kvaliteta
                total_score = (speed_score * 0.4) + (cost_score * 0.3) + (quality_score * 0.3)
                
                scored_models.append({
                    "model_name": stat.model_name,
                    "provider": stat.provider,
                    "score": total_score,
                    "speed_score": speed_score,
                    "cost_score": cost_score,
                    "quality_score": quality_score,
                    "metrics": {
                        "avg_response_time_ms": stat.avg_response_time_ms,
                        "avg_cost_usd": stat.avg_cost_usd,
                        "avg_rating": stat.avg_rating,
                        "total_summaries": stat.total_summaries
                    }
                })
            
            if not scored_models:
                raise HTTPException(
                    status_code=404,
                    detail="Ni podatkov za odločanje."
                )
            
            best = max(scored_models, key=lambda m: m["score"])
            return {
                "recommended_model": best["model_name"],
                "provider": best["provider"],
                "reason": "Uravnotežena izbira glede na hitrost, ceno in kvaliteto",
                "score": best["score"],
                "metrics": best["metrics"],
                "all_scores": scored_models
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Napaka pri odločanju: {str(e)}")


@router.get("/compare-all")
async def compare_all_models():
    """
    Primerjaj vse modele na podlagi zgodovinskih podatkov
    """
    try:
        stats = await DatabaseService.get_model_statistics()
        best_models = await DatabaseService.get_best_models_by_criteria()
        
        return {
            "statistics": [s.dict() for s in stats],
            "best_by_criteria": best_models,
            "summary": {
                "total_models": len(stats),
                "total_summaries": sum(s.total_summaries for s in stats),
                "total_cost": sum(s.total_cost_usd for s in stats)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Napaka pri primerjavi: {str(e)}")
