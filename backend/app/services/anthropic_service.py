"""
Anthropic LLM Service - Integracija z Anthropic API (Claude 3)
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
# TODO: Import anthropic
# import anthropic


class AnthropicService(LLMService):
    """Anthropic Claude LLM storitev"""
    
    def __init__(self, model_name: str = "claude-3-opus-20240229", api_key: str = ""):
        super().__init__(model_name, api_key)
        # TODO: Inicializiraj Anthropic client
        # self.client = anthropic.Anthropic(api_key=api_key)
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek z Claude modelom
        
        TODO: Implementirati podobno kot OpenAI service
        """
        raise NotImplementedError("Anthropic service not yet implemented")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek za Anthropic
        
        Cene (približno):
        - Claude 3 Opus: $0.015 per 1k input, $0.075 per 1k output
        - Claude 3 Sonnet: $0.003 per 1k input, $0.015 per 1k output
        - Claude 3 Haiku: $0.00025 per 1k input, $0.00125 per 1k output
        """
        # TODO: Implementirati izračun stroškov
        return 0.0
    
    def get_model_info(self) -> dict:
        """Vrne informacije o Anthropic modelu"""
        return {
            "id": self.model_name,
            "name": "Claude 3",
            "provider": "Anthropic",
            "supports_streaming": True,
            "max_tokens": 200000
        }

