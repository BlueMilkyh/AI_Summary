"""
OpenAI LLM Service - Integracija z OpenAI API preko OpenRouter ali direktno
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
from openai import OpenAI
from app.config import settings


class OpenAIService(LLMService):
    """OpenAI LLM storitev - uporablja OpenRouter ali direktno OpenAI API"""
    
    def __init__(self, model_name: str = "gpt-4o-mini", api_key: str = "", use_openrouter: bool = None):
        super().__init__(model_name, api_key)
        
        # Določi ali uporabimo OpenRouter
        self.use_openrouter = use_openrouter if use_openrouter is not None else settings.use_openrouter
        
        if self.use_openrouter:
            # Uporabi OpenRouter
            if not settings.openrouter_api_key:
                raise ValueError("OpenRouter API key is required. Nastavite OPENROUTER_API_KEY v config.")
            self.client = OpenAI(
                base_url=settings.openrouter_base_url,
                api_key=settings.openrouter_api_key
            )
            # OpenRouter modeli imajo format "openai/model-name"
            if not model_name.startswith("openai/"):
                self.model_name = f"openai/{model_name}"
            else:
                self.model_name = model_name
        else:
            # Uporabi direktno OpenAI API
            if not api_key:
                api_key = settings.openai_api_key
            if not api_key:
                raise ValueError("OpenAI API key is required")
            self.client = OpenAI(api_key=api_key)
            self.model_name = model_name
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek z OpenAI modelom
        """
        start_time = self._measure_time()
        
        # Ustvari prompt za povzetek
        prompt = f"Povzemi naslednje besedilo v slovenščini. Povzetek naj bo jasen in jedrnat:\n\n{text}"
        
        if max_length:
            prompt += f"\n\nPovzetek naj bo največ {max_length} znakov dolg."
        
        try:
            # Pripravi extra headers za OpenRouter (opcijsko)
            extra_headers = {}
            if self.use_openrouter:
                extra_headers = {
                    "HTTP-Referer": "http://localhost:3000",  # Vaša spletna stran
                    "X-Title": "AI Summary App"  # Ime vaše aplikacije
                }
            
            # Generiraj povzetek
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Ti si pomočnik za povzemanje besedil v slovenščini."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_length // 4 if max_length else 200,  # Približno 4 znaki na token
                extra_headers=extra_headers if extra_headers else None
            )
            
            summary = response.choices[0].message.content
            
            # Preštej tokene iz response
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            
            end_time = self._measure_time()
            
            # Ustvari metrike
            metrics = self._create_metrics(start_time, end_time, input_tokens, output_tokens)
            
            return SummaryResponse(
                summary=summary,
                model=self.model_name,
                metrics=metrics
            )
        except Exception as e:
            raise Exception(f"Napaka pri generiranju povzetka z OpenAI: {str(e)}")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek za OpenAI
        
        Cene (približno za 2025):
        - GPT-4o: $2.50 per 1M input tokens, $10.00 per 1M output tokens
        - GPT-4o-mini: $0.15 per 1M input tokens, $0.60 per 1M output tokens
        - GPT-4 Turbo: $10.00 per 1M input tokens, $30.00 per 1M output tokens
        - GPT-3.5 Turbo: $0.50 per 1M input tokens, $1.50 per 1M output tokens
        """
        model_lower = self.model_name.lower()
        
        if "gpt-4o-mini" in model_lower:
            input_cost_per_1m = 0.15
            output_cost_per_1m = 0.60
        elif "gpt-4o" in model_lower and "mini" not in model_lower:
            input_cost_per_1m = 2.50
            output_cost_per_1m = 10.00
        elif "gpt-4" in model_lower and "turbo" in model_lower:
            input_cost_per_1m = 10.00
            output_cost_per_1m = 30.00
        elif "gpt-4" in model_lower:
            # Standard GPT-4
            input_cost_per_1m = 30.00
            output_cost_per_1m = 60.00
        elif "gpt-3.5" in model_lower:
            input_cost_per_1m = 0.50
            output_cost_per_1m = 1.50
        else:
            # Privzeto - uporabi GPT-4o-mini cene
            input_cost_per_1m = 0.15
            output_cost_per_1m = 0.60
        
        input_cost = (input_tokens / 1_000_000) * input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * output_cost_per_1m
        
        return input_cost + output_cost
    
    def get_model_info(self) -> dict:
        """Vrne informacije o OpenAI modelu"""
        model_lower = self.model_name.lower()
        
        if "gpt-4o-mini" in model_lower:
            model_name_display = "GPT-4o Mini"
            max_tokens = 128000
        elif "gpt-4o" in model_lower:
            model_name_display = "GPT-4o"
            max_tokens = 128000
        elif "gpt-4" in model_lower and "turbo" in model_lower:
            model_name_display = "GPT-4 Turbo"
            max_tokens = 128000
        elif "gpt-4" in model_lower:
            model_name_display = "GPT-4"
            max_tokens = 8192
        elif "gpt-3.5" in model_lower:
            model_name_display = "GPT-3.5 Turbo"
            max_tokens = 16385
        else:
            model_name_display = "GPT-4o Mini"
            max_tokens = 128000
        
        return {
            "id": self.model_name,
            "name": model_name_display,
            "provider": "OpenAI",
            "supports_streaming": True,
            "max_tokens": max_tokens
        }

