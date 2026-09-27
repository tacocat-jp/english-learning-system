import ollama

from src.Common.config import get_config
from src.UseCase.Interface.ILLMClient import ILLMClient

class GemmaClient(ILLMClient):
    
    def generate(self, messages_) -> str:
        
        model_name = get_config('LLM', 'model_name')
        
        response = ollama.chat(
            model=model_name,
            messages=messages_,
            keep_alive=0
        )
        
        return response
    