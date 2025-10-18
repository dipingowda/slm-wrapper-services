from fastapi import Request , status
from fastapi .responses import JSONResponse
import logging

log = logging.getLogger(__name__)

class BadRequestError(ValueError):
    """For invalid inputs you detect in your code (map to 400)."""

class UpstreamError(RuntimeError):
    """For failures when calling Ollama or other dependencies (map to 502)."""

def register_error_handlers(app):
    @app.exception_handler(BadRequestError)
    async def bad_request_handler(_: Request, exc: BadRequestError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error":"bad_request","message":str(exc)},
        )
    
    @app.exception_handler(UpstreamError)
    async def upstream_handler(_:Request , exc : UpstreamError):
        #do not expose upstream error details to clients
        log.error(f"Upstream error occurred: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"error": "upstream_error", "detail": "Dependency failed"},
        )
    
    @app.exception_handler(Exception)
    async def unhandled_exception(_:Request , exc : Exception):
        log.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "internal_server_error", "detail": "An unexpected error occurred"},
        )