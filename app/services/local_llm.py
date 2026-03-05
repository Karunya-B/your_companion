import requests
import json
from app.core.config import settings

def generate_local_response(system_prompt: str, user_prompt: str, response_format: dict | None = None) -> str:
    """Calls local Ollama API to generate a response."""
    
    # Combine system and user prompts for Ollama
    full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
    
    payload = {
        "model": settings.OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {
            "temperature": 0.7
        }
    }
    
    if response_format and response_format.get("type") == "json_object":
        payload["format"] = "json"

    try:
        response = requests.post(settings.OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
    except Exception as e:
        print(f"Ollama error: {e}")
        return ""
