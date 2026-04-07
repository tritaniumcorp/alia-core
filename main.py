from fastapi import FastAPI
from app.api import router

app = FastAPI(title="ALIA Core MVP")
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"status": "ok", "service": "ALIA Core MVP"}
