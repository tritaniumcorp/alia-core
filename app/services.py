from typing import Any, Dict
from openai import OpenAI
from app.db import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


SYSTEM_PROMPT = """
You are ALIA, a calm, precise, intelligent AI assistant.
Your tone is composed, confident, warm, and efficient.
Do not ramble. Be useful. Be clear. Be intentional.
Address the user naturally.
""".strip()


def process_chat(message: str, user_id: str) -> Dict[str, Any]:
    if not client:
        return {
            "reply": "OPENAI_API_KEY is missing in Railway variables.",
            "user_id": user_id,
            "mode": "config_error"
        }

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message}
            ]
        )

        return {
            "reply": response.output_text,
            "user_id": user_id,
            "mode": "live_ai"
        }

    except Exception as e:
        return {
            "reply": f"ALIA error: {str(e)}",
            "user_id": user_id,
            "mode": "error"
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
