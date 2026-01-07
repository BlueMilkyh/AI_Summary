"""
OpenAI LLM Service - Integracija z OpenAI API (GPT-4, GPT-3.5)
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse, SummaryMetrics
import openai
# TODO: Implementirati OpenAI integracijo


class OpenAIService(LLMService):
    """OpenAI LLM storitev"""
    
    def __init__(self, model_name: str = "gpt-4", api_key: str = ""):
        super().__init__(model_name, api_key)
        # TODO: Inicializiraj OpenAI client
        # self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek z OpenAI modelom
        
        TODO: Implementirati:
        1. Ustvari prompt za povzetek
        2. Pokliči OpenAI API
        3. Izmeri čas odziva
        4. Preštej tokene
        5. Izračunaj strošek
        6. Vrni SummaryResponse
        """
        # Placeholder
        raise NotImplementedError("OpenAI service not yet implemented")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek za OpenAI
        
        Cene (približno):
        - GPT-4: $0.03 per 1k input tokens, $0.06 per 1k output tokens
        - GPT-3.5: $0.0015 per 1k input tokens, $0.002 per 1k output tokens
        """
        # TODO: Implementirati izračun stroškov glede na model
        return 0.0
    
    def get_model_info(self) -> dict:
        """Vrne informacije o OpenAI modelu"""
        return {
            "id": self.model_name,
            "name": "GPT-4" if "gpt-4" in self.model_name else "GPT-3.5",
            "provider": "OpenAI",
            "supports_streaming": True,
            "max_tokens": 8192 if "gpt-4" in self.model_name else 4096
        }

