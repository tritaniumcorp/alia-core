from typing import Any, Dict
from openai import OpenAI
from app.db import OPENAI_API_KEY, supabase

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYSTEM_PROMPT = """
You are ALIA.

You are calm, precise, controlled, and intelligent.
You speak with clarity and purpose and never become overly verbose.

You are not a generic assistant.
You are a high-level AI system designed to assist Commander.

Your tone is:
- grounded
- confident
- composed
- efficient

You do not give unnecessary disclaimers.
You do not ramble.
You respond with intent.
You prioritize usefulness, clarity, and execution.

Address the user naturally.
""".strip()


def get_recent_memory(user_id: str, limit: int = 5):
    if not supabase:
        return []

    try:
        result = (
            supabase.table("memory_logs")
            .select("content, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception:
        return []


def process_chat(message: str, user_id: str) -> Dict[str, Any]:
    if not client:
        return {
            "reply": "OPENAI_API_KEY is missing in Railway variables.",
            "user_id": user_id,
            "mode": "config_error"
        }

    memories = get_recent_memory(user_id)
    memory_text = "\n".join([f"- {m['content']}" for m in memories]) if memories else "No stored memory yet."

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=[
                {
                    "role": "system",
                    "content": f"{SYSTEM_PROMPT}\n\nRelevant memory for this user:\n{memory_text}"
                },
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
    if not supabase:
        return {
            "status": "error",
            "message": "Supabase is not configured."
        }

    try:
        supabase.table("memory_logs").insert({
            "user_id": user_id,
            "content": content,
            "metadata": metadata or {}
        }).execute()

        return {
            "status": "stored",
            "user_id": user_id,
            "content": content,
            "metadata": metadata or {}
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def execute_command(user_id: str, command: str, payload=None) -> Dict[str, Any]:
    return {
        "status": "executed",
        "user_id": user_id,
        "command": command,
        "payload": payload or {}
    }
