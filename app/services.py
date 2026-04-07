from typing import Any, Dict


def process_chat(message: str, user_id: str) -> Dict[str, Any]:
    return {
        "reply": f"ALIA received: {message}",
        "user_id": user_id,
        "mode": "mvp"
    }


def store_memory(user_id: str, content: str, metadata=None) -> Dict[str, Any]:
    return {
        "status": "stored",
        "user_id": user_id,
        "content": content,
        "metadata": metadata or {}
    }


def execute_command(user_id: str, command: str, payload=None) -> Dict[str, Any]:
    return {
        "status": "executed",
        "user_id": user_id,
        "command": command,
        "payload": payload or {}
    }
