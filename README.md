# 🧩 Local LLM API Server (FastAPI + Ollama)

A lightweight, production-style backend for running **local LLMs** through a clean HTTP API.  
Built with **FastAPI**, connected to a local **Ollama** instance (e.g. `phi3:mini`, `llama3`, etc.), and includes all core backend fundamentals:
- Async streaming responses
- Structured logging & request IDs
- Centralized error handling
- JSONL + CSV + SQLite audit logging
- Modular project layout for easy scaling

---

## 🚀 Features

| Category | Description |
|-----------|-------------|
| 🧠 **LLM Integration** | Uses [Ollama](https://ollama.ai) as the local model backend |
| ⚡ **Async Streaming** | Real-time token streaming with `StreamingResponse` |
| 📜 **Logging** | Request-ID based access logs, structured JSON logs |
| 💾 **Audit Logging** | Stores every request (prompt length, duration, etc.) in JSONL, CSV, and SQLite |
| 🧩 **Error Handling** | Centralized exceptions → clean JSON responses |
| 🔐 **Auth (Optional)** | Header-based API key (toggle in config) |
| ⚙️ **Configurable** | All paths & toggles can move to `pydantic-settings` later |

---
## 🧩 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | Root endpoint |
| `/healthz` | GET | Liveness check |
| `/readyz` | GET | Verifies Ollama availability |
| `/generate` | POST | Generate full text (non-streaming) |
| `/generate/stream` | POST | Stream generated tokens live |

---

### 🔧 Example Request

```
curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain caching in 3 points.", "model": "phi3:mini"}'
🌀 Streaming

Copy code
curl -N -X POST http://127.0.0.1:8000/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write 3 good backend habits.", "model": "phi3:mini"}'
🧠 How It Works
FastAPI receives your prompt → sends to local Ollama server (http://127.0.0.1:11434/api/generate)

Ollama streams tokens back → StreamingResponse relays them chunk-by-chunk

Access + Audit log middlewares record request metadata:

request ID, endpoint, latency, token count, model used, status

Audit data is written to:

logs/audit.jsonl (newline JSON)

logs/audit.csv

logs/audit.sqlite

Errors are caught globally → formatted JSON output.

⚙️ Running Locally
Install Ollama


https://ollama.ai/download
Start Ollama daemon (default port 11434):


ollama serve
Pull a model (example):


ollama pull phi3:mini
Create virtual env

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Run FastAPI


uvicorn app.main:app --reload --port 8000

Use postman/curl for endpoint testing
Note : For stream use curl on terminal because postman is poor at handling stream responses

Format for curl requests:
curl -N -X POST http://127.0.0.1:8000/generate/stream ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"<prompt-here>\",\"model\":\"phi3:mini\"}"
