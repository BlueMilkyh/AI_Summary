"""
Google LLM Service - Integracija z Google AI API (Gemini Pro)
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
import google.generativeai as genai


class GoogleService(LLMService):
    """Google Gemini LLM storitev"""
    
    def __init__(self, model_name: str = "gemini-pro", api_key: str = ""):
        super().__init__(model_name, api_key)
        if not api_key:
            raise ValueError("Google API key is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek z Gemini modelom
        """
        start_time = self._measure_time()
        
        # Ustvari prompt za povzetek
        prompt = f"Povzemi naslednje besedilo v slovenščini. Povzetek naj bo jasen in jedrnat:\n\n{text}"
        
        if max_length:
            prompt += f"\n\nPovzetek naj bo največ {max_length} znakov dolg."
        
        try:
            # Generiraj povzetek
            response = self.model.generate_content(prompt)
            summary = response.text
            
            # Preštej tokene (približno: 1 token ≈ 4 znaki)
            # Google API ne vrača natančnega števila tokenov v vseh verzijah,
            # zato uporabimo približek
            input_tokens = len(text) // 4
            output_tokens = len(summary) // 4
            
            end_time = self._measure_time()
            
            # Ustvari metrike
            metrics = self._create_metrics(start_time, end_time, input_tokens, output_tokens)
            
            return SummaryResponse(
                summary=summary,
                model=self.model_name,
                metrics=metrics
            )
        except Exception as e:
            raise Exception(f"Napaka pri generiranju povzetka z Gemini: {str(e)}")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek za Google Gemini
        
        Cene (približno):
        - Gemini Pro: $0.0005 per 1k input, $0.0015 per 1k output
        - Gemini 1.5 Pro: $0.00125 per 1k input, $0.005 per 1k output
        """
        # Preveri verzijo modela
        if "1.5" in self.model_name.lower() or "gemini-1.5" in self.model_name.lower():
            input_cost_per_1k = 0.00125
            output_cost_per_1k = 0.005
        else:
            # Standard Gemini Pro cene
            input_cost_per_1k = 0.0005
            output_cost_per_1k = 0.0015
        
        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k
        
        return input_cost + output_cost
    
    def get_model_info(self) -> dict:
        """Vrne informacije o Google modelu"""
        model_name_display = "Gemini Pro"
        if "1.5" in self.model_name.lower():
            model_name_display = "Gemini 1.5 Pro"
        elif "gemini-pro" in self.model_name.lower():
            model_name_display = "Gemini Pro"
        
        return {
            "id": self.model_name,
            "name": model_name_display,
            "provider": "Google",
            "supports_streaming": False,
            "max_tokens": 32768
        }

