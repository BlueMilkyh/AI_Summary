"""
Abstraktna osnovna klasa za LLM storitve
Vsi LLM servisi morajo implementirati ta interface
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.schemas.summary import SummaryResponse, SummaryMetrics
from datetime import datetime
import time


class LLMService(ABC):
    """Abstraktna osnovna klasa za LLM storitve"""
    
    def __init__(self, model_name: str, api_key: str):
        self.model_name = model_name
        self.api_key = api_key
    
    @abstractmethod
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek besedila
        
        Args:
            text: Besedilo za povzetek
            max_length: Maksimalna dolžina povzetka (opcijsko)
            
        Returns:
            SummaryResponse z povzetkom in metrikami
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek na podlagi števila tokenov
        
        Args:
            input_tokens: Število vhodnih tokenov
            output_tokens: Število izhodnih tokenov
            
        Returns:
            Strošek v USD
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        Vrne informacije o modelu
        
        Returns:
            Dictionary z informacijami (name, provider, max_tokens, itd.)
        """
        pass
    
    def _measure_time(self) -> float:
        """Pomožna metoda za merjenje časa"""
        return time.time()
    
    def _create_metrics(
        self, 
        start_time: float, 
        end_time: float,
        input_tokens: int,
        output_tokens: int
    ) -> SummaryMetrics:
        """Ustvari SummaryMetrics objekt"""
        response_time_ms = (end_time - start_time) * 1000
        total_tokens = input_tokens + output_tokens
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        return SummaryMetrics(
            response_time_ms=response_time_ms,
            tokens_used=total_tokens,
            cost_usd=cost,
            timestamp=datetime.now()
        )

