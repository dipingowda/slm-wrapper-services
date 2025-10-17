from typing import AsyncIterator
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.generate import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService

router = APIRouter(prefix="/generate", tags=["llm"])
svc = LLMService()

@router.post("",response_model=GenerateResponse,status_code=200)
async def generate(body:GenerateRequest) ->GenerateResponse:
    text = await svc.generateOnce(body.model, body.prompt)
    return GenerateResponse(prompt=body.prompt, model=body.model, response=text)

@router.post("/stream",status_code=200)
async def generate_stream(body:GenerateRequest):
    async def iter_chunks() -> AsyncIterator[str]:
        async for chunk in svc.generateStream(body.model, body.prompt):
            yield chunk

    return StreamingResponse(iter_chunks(), media_type="text/event-stream")