# ALIA Core MVP

Minimal FastAPI backend for ALIA AI.

## Endpoints
- `GET /`
- `POST /api/v1/chat`
- `POST /api/v1/memory/store`
- `POST /api/v1/command/execute`

## Run locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
