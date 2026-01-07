"""
Hugging Face LLM Service - Integracija z Hugging Face API
"""
from typing import Optional
from app.services.llm_service import LLMService
from app.schemas.summary import SummaryResponse
# TODO: Import huggingface
# from huggingface_hub import InferenceClient


class HuggingFaceService(LLMService):
    """Hugging Face LLM storitev (LLaMA, Mistral, itd.)"""
    
    def __init__(self, model_name: str = "meta-llama/Llama-2-7b-chat-hf", api_key: str = ""):
        super().__init__(model_name, api_key)
        # TODO: Inicializiraj Hugging Face client
        # self.client = InferenceClient(model=model_name, token=api_key)
    
    async def generate_summary(
        self, 
        text: str, 
        max_length: Optional[int] = None
    ) -> SummaryResponse:
        """
        Generira povzetek z Hugging Face modelom
        
        TODO: Implementirati podobno kot OpenAI service
        Opomba: Hugging Face API ima lahko drugačen format
        """
        raise NotImplementedError("Hugging Face service not yet implemented")
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Izračuna strošek za Hugging Face
        
        Opomba: Cene so odvisne od modela in načina uporabe
        Nekateri modeli so brezplačni za omejeno število klicev
        """
        # TODO: Implementirati izračun stroškov (lahko 0.0 za brezplačne modele)
        return 0.0
    
    def get_model_info(self) -> dict:
        """Vrne informacije o Hugging Face modelu"""
        return {
            "id": self.model_name,
            "name": "LLaMA 2",
            "provider": "Hugging Face",
            "supports_streaming": False,
            "max_tokens": 4096
        }

