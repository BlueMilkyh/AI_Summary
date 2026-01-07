"""
Google LLM Service - Integracija z Google AI API (Gemini)
"""
from typing import Optional, List
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
from google import genai
import os


class GoogleService(LLMService):
    """Google Gemini LLM storitev"""
    
    def __init__(self, model_name: str = "gemini-2.5-flash", api_key: str = ""):
        super().__init__(model_name, api_key)
        if not api_key:
            raise ValueError("Google API key is required")
        
        # Nastavi API ključ kot environment variable ali uporabi direktno
        os.environ["GEMINI_API_KEY"] = api_key
        self.client = genai.Client(api_key=api_key)
        
        # Najprej preveri, kateri modeli so na voljo
        available_models = self._get_available_models()
        
        # Če je podan model na seznamu na voljo, ga uporabi
        if model_name in available_models:
            self.model_name = model_name
        elif available_models:
            # Če podan model ni na voljo, uporabi prvi na voljo model
            self.model_name = available_models[0]
        else:
            # Fallback na privzeti model
            self.model_name = model_name if model_name else "gemini-2.5-flash"
    
    def _get_available_models(self) -> List[str]:
        """Vrne seznam na voljo modelov"""
        try:
            # Novi API - poskusi pridobiti modele
            models = self.client.models.list()
            available = []
            for model in models:
                # Modeli so objekti z imenom
                if hasattr(model, 'name'):
                    model_name = model.name.replace('models/', '')
                    available.append(model_name)
            return available if available else ["gemini-2.5-flash"]
        except Exception:
            # Fallback seznam novih modelov
            return ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash", "gemini-1.5-pro"]
    
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
            # Generiraj povzetek z novim API-jem
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            summary = response.text
            
            # Preštej tokene - poskusimo dobiti natančno število iz response
            input_tokens = len(text) // 4  # Približek
            output_tokens = len(summary) // 4  # Približek
            
            # Poskusimo dobiti natančno število tokenov če je na voljo
            if hasattr(response, 'usage_metadata'):
                if hasattr(response.usage_metadata, 'prompt_token_count'):
                    input_tokens = response.usage_metadata.prompt_token_count
                if hasattr(response.usage_metadata, 'candidates_token_count'):
                    output_tokens = response.usage_metadata.candidates_token_count
            elif hasattr(response, 'usage'):
                # Alternativni format za usage
                if hasattr(response.usage, 'prompt_token_count'):
                    input_tokens = response.usage.prompt_token_count
                if hasattr(response.usage, 'total_token_count'):
                    # Če imamo samo skupno, ocenimo output
                    total = response.usage.total_token_count
                    output_tokens = max(0, total - input_tokens)
            
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
        
        Cene (približno za 2025):
        - Gemini 2.5 Flash: $0.075 per 1M input, $0.30 per 1M output
        - Gemini 2.5 Pro: $1.25 per 1M input, $5.00 per 1M output
        - Gemini 2.0 Flash: $0.075 per 1M input, $0.30 per 1M output (približno kot 2.5 Flash)
        """
        # Preveri verzijo modela
        model_lower = self.model_name.lower()
        if "2.5" in model_lower or "2-5" in model_lower:
            if "flash" in model_lower:
                # Gemini 2.5 Flash
                input_cost_per_1m = 0.075
                output_cost_per_1m = 0.30
            elif "pro" in model_lower:
                # Gemini 2.5 Pro
                input_cost_per_1m = 1.25
                output_cost_per_1m = 5.00
            else:
                # Privzeto za 2.5
                input_cost_per_1m = 0.075
                output_cost_per_1m = 0.30
        elif "2.0" in model_lower or "2-0" in model_lower:
            if "flash" in model_lower:
                # Gemini 2.0 Flash
                input_cost_per_1m = 0.075
                output_cost_per_1m = 0.30
            else:
                # Privzeto za 2.0
                input_cost_per_1m = 0.075
                output_cost_per_1m = 0.30
        else:
            # Privzeto - uporabi Flash cene
            input_cost_per_1m = 0.075
            output_cost_per_1m = 0.30
        
        input_cost = (input_tokens / 1_000_000) * input_cost_per_1m
        output_cost = (output_tokens / 1_000_000) * output_cost_per_1m
        
        return input_cost + output_cost
    
    def get_model_info(self) -> dict:
        """Vrne informacije o Google modelu"""
        model_lower = self.model_name.lower()
        if "2.5" in model_lower or "2-5" in model_lower:
            if "flash" in model_lower:
                model_name_display = "Gemini 2.5 Flash"
                max_tokens = 1048576  # 1M tokenov
            elif "pro" in model_lower:
                model_name_display = "Gemini 2.5 Pro"
                max_tokens = 2097152  # 2M tokenov
            else:
                model_name_display = "Gemini 2.5 Flash"
                max_tokens = 1048576
        elif "2.0" in model_lower or "2-0" in model_lower:
            if "flash" in model_lower:
                model_name_display = "Gemini 2.0 Flash"
                max_tokens = 1048576  # 1M tokenov
            else:
                model_name_display = "Gemini 2.0 Flash"
                max_tokens = 1048576
        elif "flash" in model_lower:
            model_name_display = "Gemini 1.5 Flash"
            max_tokens = 1048576  # 1M tokenov
        elif "1.5-pro" in model_lower or "1.5pro" in model_lower:
            model_name_display = "Gemini 1.5 Pro"
            max_tokens = 2097152  # 2M tokenov
        else:
            model_name_display = "Gemini 2.5 Flash"
            max_tokens = 1048576
        
        return {
            "id": self.model_name,
            "name": model_name_display,
            "provider": "Google",
            "supports_streaming": False,
            "max_tokens": max_tokens
        }
    
    @staticmethod
    def list_available_models(api_key: str) -> List[dict]:
        """Statična metoda za pridobitev seznama na voljo modelov"""
        try:
            os.environ["GEMINI_API_KEY"] = api_key
            client = genai.Client(api_key=api_key)
            models = client.models.list()
            available = []
            for model in models:
                model_name = model.name.replace('models/', '') if hasattr(model, 'name') else str(model)
                available.append({
                    "id": model_name,
                    "name": getattr(model, 'display_name', model_name) or model_name,
                    "provider": "Google",
                    "supports_streaming": False,
                    "max_tokens": getattr(model, 'input_token_limit', 1048576),
                    "status": "available"
                })
            return available if available else [
                {
                    "id": "gemini-2.5-flash",
                    "name": "Gemini 2.5 Flash",
                    "provider": "Google",
                    "supports_streaming": False,
                    "max_tokens": 1048576,
                    "status": "available"
                }
            ]
        except Exception as e:
            # Fallback na znane nove modele
            return [
                {
                    "id": "gemini-2.5-flash",
                    "name": "Gemini 2.5 Flash",
                    "provider": "Google",
                    "supports_streaming": False,
                    "max_tokens": 1048576,
                    "status": "available"
                },
                {
                    "id": "gemini-2.5-pro",
                    "name": "Gemini 2.5 Pro",
                    "provider": "Google",
                    "supports_streaming": False,
                    "max_tokens": 2097152,
                    "status": "available"
                },
                {
                    "id": "gemini-1.5-flash",
                    "name": "Gemini 1.5 Flash",
                    "provider": "Google",
                    "supports_streaming": False,
                    "max_tokens": 1048576,
                    "status": "available"
                }
            ]

