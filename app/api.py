from fastapi import APIRouter
from app.schemas import ChatRequest, MemoryStoreRequest, CommandRequest
from app.services import process_chat, store_memory, execute_command

router = APIRouter()


@router.post("/chat")
def chat(req: ChatRequest):
    return process_chat(req.message, req.user_id)


@router.post("/memory/store")
def memory_store(req: MemoryStoreRequest):
    return store_memory(req.user_id, req.content, req.metadata)


@router.post("/command/execute")
def command_execute(req: CommandRequest):
    return execute_command(req.user_id, req.command, req.payload)
