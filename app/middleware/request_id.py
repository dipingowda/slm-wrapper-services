import uuid 
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

REQUEST_ID_HEADER = "X-Request-ID"

class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to assign a unique request ID to each incoming HTTP request.
    The request ID is added to the request state and can be included in log records.
    """
    async def dispatch(self,request:Request,call_next):
        req_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        # Attach request ID to request state
        request.state.request_id = req_id  
        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = req_id
        return response
    
    