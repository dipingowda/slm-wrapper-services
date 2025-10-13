from fastapi import FastAPI,status
import uvicorn
from app.schema import GenerateRequest,GenerateResponse
from dotenv import load_dotenv
import httpx

load_dotenv('G:/slm-wrapper/.env.local')

app = FastAPI(title="Local LLM API Server", version="1.0")
OLLAMA_BASE = "http://127.0.0.1:11434"

#basic endpoints
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "ok",
        "message": "The local llm api server is up and running",
    }

@app.get("/ready",status_code = status.HTTP_200_OK)
def readyserver():
    return {
        "status": "ready",
        "message": "The local llm api server is ready to take requests",
    }

@app.get("/")
def read_root():
    return {
        "message": "This the root endpoint for the local llm api server",
        "status": 200
    }





@app.post("/generate",response_model=GenerateResponse,status_code=status.HTTP_200_OK)
def generate(body: GenerateRequest):
    """
    This endpoints pings the POST /generate endpoint with stream set to false which returns the full response at once.
    The response is then returned to the client.
    """
    payload = {
        "model": body.model,
        "prompt": body.prompt,
        "stream": False,
    }

    try:
        r= httpx.post(f"{OLLAMA_BASE}/api/generate",json=payload,timeout=60)
        r.raise_for_status()
        data = r.json()
        text = (data.get("response") or "").rstrip()
    except httpx.HTTPError as e:
        text = f"Error: {str(e)}"
    return GenerateResponse(prompt=body.prompt, model=body.model, response=text)









if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info")