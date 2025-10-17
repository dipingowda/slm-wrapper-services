from fastapi import FastAPI
from app.routers.health import router as health_router
from app.routers.generate import router as generate_router

app = FastAPI(title="Local LLM API Server", version="1.0")

app.include_router(health_router)
app.include_router(generate_router)