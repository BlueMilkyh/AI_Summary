"""
Anthropic LLM Service - Integracija z Anthropic API preko OpenRouter
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
from openai import OpenAI
from app.config import settings


class AnthropicService(LLMService):
    """Anthropic Claude LLM storitev - uporablja OpenRouter API"""
    
    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", api_key: str = ""):
        super().__init__(model_name, api_key)
        
        if not settings.openrouter_api_key:
            raise ValueError("OpenRouter API key is required. Nastavite OPENROUTER_API_KEY v config.")
        
        self.client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key
        )
        
        # OpenRouter modeli imajo format "anthropic/model-name"
        if not model_name.startswith("anthropic/"):
            self.model_name = f"anthropic/{model_name}"
        else:
            self.model_name = model_name
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """Generira povzetek z Claude modelom preko OpenRouterja"""
        start_time = self._measure_time()
        
        prompt = f"Povzemi naslednje besedilo v slovenščini. Povzetek naj bo jasen in jedrnat:\n\n{text}"
        if max_length:
            prompt += f"\n\nPovzetek naj bo največ {max_length} znakov dolg."
        
        try:
            extra_headers = {
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "AI Summary App"
            }
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Ti si pomočnik za povzemanje besedil v slovenščini."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length // 4 if max_length else 200,
                extra_headers=extra_headers
            )
            
            summary = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            end_time = self._measure_time()
            
            metrics = self._create_metrics(start_time, end_time, input_tokens, output_tokens)
            
            return SummaryResponse(
                summary=summary,
                model=self.model_name,
                metrics=metrics
            )
        except Exception as e:
            raise Exception(f"Napaka pri generiranju povzetka z Claude: {str(e)}")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Izračuna strošek za Anthropic modele preko OpenRouterja"""
        model_lower = self.model_name.lower()
        
        if "3.5" in model_lower or "3-5" in model_lower:
            if "sonnet" in model_lower:
                input_cost_per_1m = 3.00
                output_cost_per_1m = 15.00
            else:
                input_cost_per_1m = 3.00
                output_cost_per_1m = 15.00
        else:
            input_cost_per_1m = 3.00
            output_cost_per_1m = 15.00
        
        input_cost = (input_tokens / 1_000_000) * input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * output_cost_per_1m
        
        return input_cost + output_cost
    
    def get_model_info(self) -> dict:
        """Vrne informacije o Anthropic modelu"""
        model_lower = self.model_name.lower()
        
        if "3.5" in model_lower or "3-5" in model_lower:
            model_name_display = "Claude 3.5 Sonnet"
        else:
            model_name_display = "Claude 3.5 Sonnet"
        
        return {
            "id": self.model_name,
            "name": model_name_display,
            "provider": "Anthropic",
            "supports_streaming": True,
            "max_tokens": 200000
        }
