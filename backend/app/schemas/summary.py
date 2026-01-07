"""
Pydantic sheme za povzetke - Request/Response modeli
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class SummaryRequest(BaseModel):
    """Zahteva za generiranje povzetka"""
    text: str = Field(..., description="Besedilo za povzetek", min_length=10)
    model: str = Field(..., description="Ime LLM modela (npr. 'gpt-4', 'claude-3')")
    max_length: Optional[int] = Field(None, description="Maksimalna dolžina povzetka v znakih")
    language: Optional[str] = Field("sl", description="Jezik povzetka")


class SummaryMetrics(BaseModel):
    """Metrike za povzetek"""
    response_time_ms: float = Field(..., description="Čas odziva v milisekundah")
    tokens_used: int = Field(..., description="Število uporabljenih tokenov")
    cost_usd: float = Field(..., description="Strošek v USD")
    timestamp: datetime = Field(default_factory=datetime.now)


class SummaryResponse(BaseModel):
    """Odgovor z generiranim povzetkom"""
    summary: str = Field(..., description="Generirani povzetek")
    model: str = Field(..., description="Uporabljeni model")
    metrics: SummaryMetrics = Field(..., description="Metrike generiranja")


class ComparisonRequest(BaseModel):
    """Zahteva za primerjavo več modelov"""
    text: str = Field(..., description="Besedilo za povzetek", min_length=10)
    models: List[str] = Field(..., description="Seznam modelov za primerjavo", min_items=2)
    max_length: Optional[int] = Field(None, description="Maksimalna dolžina povzetka")


class ComparisonResult(BaseModel):
    """Rezultat primerjave"""
    fastest: str = Field(..., description="Najhitrejši model")
    cheapest: str = Field(..., description="Najcenejši model")
    average_response_time: float = Field(..., description="Povprečen čas odziva")
    total_cost: float = Field(..., description="Skupni strošek")


class ComparisonResponse(BaseModel):
    """Odgovor z rezultati primerjave"""
    results: List[SummaryResponse] = Field(..., description="Rezultati za vsak model")
    comparison: ComparisonResult = Field(..., description="Primerjava modelov")

