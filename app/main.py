from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.generate import router as generate_router


from app.errors import register_error_handlers
from app.logging_setup import setup_logging
from app.middleware.access_log import AccessLogMiddleware
from app.middleware.request_id import RequestIDMiddleware

from app.telemetry.audit import AuditLogger

app = FastAPI(title="Local LLM API Server", version="1.0")
# Logging first
setup_logging()

#Middlewares
app.add_middleware(AccessLogMiddleware)
app.add_middleware(RequestIDMiddleware)


#Create a single audit sink and attach to app.state
app.state.audit = AuditLogger(
    jsonl_path="logs/audit.jsonl",
    csv_path="logs/audit.csv",
    sqlite_path="logs/audit.sqlite",
)

#Routers
app.include_router(health_router)
app.include_router(generate_router)

#Error Handlers(after routers to catch errors)
register_error_handlers(app)