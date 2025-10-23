# 🧩 Local LLM API Server (FastAPI + Ollama)

A lightweight, production-style backend for running **local LLMs** through a clean HTTP API.  
Built with open source technologies like **FastAPI**, connected to a local **Ollama** instance (e.g. `phi3:mini`, `llama3`, etc.), and includes all core backend fundamentals:
- Async streaming responses
- Structured logging & request IDs
- Centralised error handling
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

---
## 🧩 API Endpoints

| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/` | GET | Root endpoint |
| `/health` | GET | Liveness check |
| `/ready` | GET | Verifies Ollama availability |
| `/generate` | POST | Generate full text (non-streaming) |
| `/generate/stream` | POST | Stream generated tokens live |

---

### 🔧 Example Request

🌀 Streaming
```
curl -N -X POST http://127.0.0.1:8000/generate/stream \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write 3 good backend habits.", "model": "phi3:mini"}'
```
🧠 How It Works
FastAPI receives your prompt → sends to local Ollama server (http://127.0.0.1:11434/api/generate)

Ollama streams tokens back → StreamingResponse relays them chunk-by-chunk

Access + Audit log middleware records request metadata:

request ID, endpoint, latency, token count, model used, status

Audit data is written to:

|logs/audit.jsonl (newline JSON)|

|logs/audit.csv|

|logs/audit.sqlite|

Errors are caught globally → formatted JSON output.

# ⚙️ Running Locally

### Install Ollama
```
https://ollama.ai/download
```
### Start Ollama daemon (default port 11434):
```
ollama serve
```

### Pull a model (example):
```
ollama pull phi3:mini
```

### Create virtual env
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run FastAPI
```
uvicorn app.main:app --reload --port 8000
```

### Use Postman/curl for endpoint testing
### Note: For stream use curl on the terminal because Postman is poor at handling stream responses

### Format for curl requests:
```
curl -N -X POST http://127.0.0.1:8000/generate/stream ^
  -H "Content-Type: application/json" ^
  -d "{\"prompt\":\"<prompt-here>\",\"model\":\"phi3:mini\"}"
```
---

## 🧑‍💻 Contributing
Contributions, ideas, and feedback are welcome!

If you’d like to:
- improve the backend structure
- add Docker / SSE / UI support
- or test new Ollama models

Feel free to fork the repo, open a PR, or reach out.

You can also open issues for feature suggestions or bug reports.

---

## 🧩 Open Source Notice

This project is built entirely using **open-source technologies** — it does not modify, redistribute, or claim ownership over them.

Core dependencies:
- [FastAPI](https://fastapi.tiangolo.com/) — web framework (MIT License)
- [Uvicorn](https://www.uvicorn.org/) — ASGI server (BSD License)
- [HTTPX](https://www.python-httpx.org/) — async HTTP client (BSD License)
- [Pydantic](https://docs.pydantic.dev/) — data validation (MIT License)
- [Ollama](https://ollama.ai) — local model runtime (MIT License)

This repository simply integrates these tools into a cohesive, modular backend for local AI experimentation.  
All credit for the underlying libraries and model runtimes belongs to their respective creators and maintainers.

---
