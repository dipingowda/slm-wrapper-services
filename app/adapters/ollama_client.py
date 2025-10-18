import json 
from typing import AsyncIterator
import httpx

from app.errors import UpstreamError

class OllamaClient:
    def __init__(self,base_url:str ="http://127.0.0.1:11434",timeout:float = 120.0):
        self.base_url = base_url
        self.timeout = timeout

    async def generateStream(self,model:str , prompt:str) -> AsyncIterator[str]:
        payload ={
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as Client:
                async with Client.stream("POST",f"{self.base_url}/api/generate",json=payload) as res:
                    res.raise_for_status()
                    async for line in res.aiter_lines():
                        if not line :
                            continue
                        try:
                            obj = json.loads(line)
                            chunk = obj.get("response") or ""
                            if chunk:
                                yield chunk
                            if obj.get("done"):
                                break
                        except Exception:
                            continue
        except httpx.HTTPError as e:
            raise UpstreamError(f"Ollama request failed: {str(e)}") from e

    async def generateOnce(self,model:str,prompt:str) ->str:
        payload ={
            "model":model,
            "prompt":prompt,
            "stream": False
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as Client:
                res = await Client.post(f"{self.base_url}/api/generate",json=payload)
                res.raise_for_status()
                data = res.json()
                return  (data.get("response") or "").rstrip()
        except httpx.HTTPError as e:
            raise UpstreamError(f"Ollama request failed: {str(e)}") from e
