from typing import AsyncIterator
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

from app.models.generate import GenerateRequest, GenerateResponse
from app.services.llm_service import LLMService

from time import perf_counter
import logging 

log = logging.getLogger(__name__)

router = APIRouter(prefix="/generate", tags=["llm"])
svc = LLMService()

@router.post("", response_model=GenerateResponse, status_code=200)
async def generate(body: GenerateRequest, request: Request) -> GenerateResponse:
    start = perf_counter()
    status = "ok"

    text = ""
    try:
        text = await svc.generateOnce(body.model, body.prompt)
        return GenerateResponse(prompt=body.prompt, model=body.model, response=text)
    except Exception as e:
        status = "error"
        raise 
    finally:
        dur = int((perf_counter() - start) * 1000)
        req_id = request.state.request_id 
        request.app.state.audit.log({
            "request_id": req_id,
            "endpoint": "/generate",
            "model": body.model,
            "prompt_len": len(body.prompt),
            "response_len": len(text),
            "status": status,
            "duration_ms": dur,
            "stream": False,
        })


@router.post("/stream", status_code=200)
async def generate_stream(body: GenerateRequest, request: Request):

    start = perf_counter()
    req_id = getattr(request.state, "request_id", "-")
    total_len = 0
    status = "ok"

    
    async def iter_chunks() -> AsyncIterator[str]:
        nonlocal total_len, status
        try:
            async for chunk in svc.generateStream(body.model, body.prompt):
                total_len += len(chunk)
                yield chunk
        except Exception as e:
            status = "error"
            raise
        finally:
            dur = int((perf_counter() - start) * 1000)
            request.app.state.audit.log({
                "request_id": req_id,
                "endpoint": "/generate/stream",
                "model": body.model,
                "prompt_len": len(body.prompt),
                "response_len": total_len,
                "status": status,
                "duration_ms": dur,
                "stream": True,
            })

    return StreamingResponse(iter_chunks(), media_type="text/event-stream")