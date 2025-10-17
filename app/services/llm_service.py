from typing import AsyncIterator
from app.adapters.ollama_client import OllamaClient   

class LLMService:
    def __init__(self , client:OllamaClient | None = None):
        self.client = client or OllamaClient()

    async def generateOnce(self , model:str , prompt:str) -> str:
            return await self.client.generateOnce(model,prompt)
        
    async def generateStream(self , model:str , prompt:str) -> AsyncIterator[str]:
            async for chunk in self.client.generateStream(model,prompt):
                yield chunk
