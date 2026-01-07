"""
Pomožne funkcije za merjenje metrik
"""
from typing import List, Dict
from app.schemas.summary import SummaryResponse, ComparisonResult


def calculate_comparison(results: List[SummaryResponse]) -> ComparisonResult:
    """
    Izračuna primerjavo med rezultati različnih modelov
    
    Args:
        results: Seznam SummaryResponse objektov
        
    Returns:
        ComparisonResult z najhitrejšim, najcenejšim, itd.
    """
    if not results:
        raise ValueError("Results list cannot be empty")
    
    # Najhitrejši model
    fastest = min(results, key=lambda r: r.metrics.response_time_ms)
    
    # Najcenejši model
    cheapest = min(results, key=lambda r: r.metrics.cost_usd)
    
    # Povprečen čas odziva
    avg_time = sum(r.metrics.response_time_ms for r in results) / len(results)
    
    # Skupni strošek
    total_cost = sum(r.metrics.cost_usd for r in results)
    
    return ComparisonResult(
        fastest=fastest.model,
        cheapest=cheapest.model,
        average_response_time=avg_time,
        total_cost=total_cost
    )


def format_metrics_for_display(metrics: Dict) -> Dict:
    """
    Formatira metrike za prikaz v frontend-u
    
    TODO: Implementirati formatiranje
    """
    return metrics

