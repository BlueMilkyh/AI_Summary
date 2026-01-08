"""
Database models za Supabase
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class SummaryRecord(BaseModel):
    """Model za shranjevanje povzetka v bazi"""
    id: Optional[UUID] = None
    original_text: str
    summary_text: str
    model_name: str
    provider: str
    response_time_ms: float
    tokens_used: int
    cost_usd: float
    max_length: Optional[int] = None
    language: str = "sl"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ModelComparisonRecord(BaseModel):
    """Model za shranjevanje primerjave modelov"""
    id: Optional[UUID] = None
    original_text: str
    comparison_data: Dict[str, Any]
    fastest_model: Optional[str] = None
    cheapest_model: Optional[str] = None
    average_response_time: Optional[float] = None
    total_cost: Optional[float] = None
    created_at: Optional[datetime] = None


class UserRatingRecord(BaseModel):
    """Model za uporabniške ocene"""
    id: Optional[UUID] = None
    summary_id: UUID
    model_name: str
    rating: int  # 1-5
    feedback: Optional[str] = None
    created_at: Optional[datetime] = None


class ModelStatistics(BaseModel):
    """Model za statistike modela"""
    model_name: str
    provider: str
    total_summaries: int
    avg_response_time_ms: float
    avg_cost_usd: float
    avg_tokens_used: float
    total_cost_usd: float
    min_response_time_ms: float
    max_response_time_ms: float
    avg_rating: Optional[float] = None
    total_ratings: int = 0
