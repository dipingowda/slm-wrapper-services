import time 
import logging 
from httpx import request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

log = logging.getLogger("access")

class AccessLogMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log access details for each incoming HTTP request.
    Logs method, path, status code, processing time, and request ID.
    """
    async def dispatch(self, request:Request, call_next):
        start = time.perf_counter()

        # Provide request_id to logging via a custom attribute
        request_id = getattr(request.state, "request_id", "-")
        extra = {"request_id": request_id}

        log.info("REQ %s %s", request.method, request.url.path, extra=extra)

        response = await call_next(request)

        duration_ms = int((time.perf_counter() - start) * 1000)
        # Stuff some helpful headers
        response.headers["X-Response-Time-ms"] = str(duration_ms)
        response.headers["X-Request-ID"] = request_id  # echo back to client
        log.info(
            "RES %s %s %s %dms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra=extra,
        )
        return response