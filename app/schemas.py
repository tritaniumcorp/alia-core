from pydantic import BaseModel
from typing import Optional, Dict, Any


class ChatRequest(BaseModel):
    message: str
    user_id: str


class MemoryStoreRequest(BaseModel):
    user_id: str
    content: str
    metadata: Optional[Dict[str, Any]] = None


class CommandRequest(BaseModel):
    user_id: str
    command: str
    payload: Optional[Dict[str, Any]] = None
