import requests
from app.core.config import settings

def generate_response(prompt: str):
    """Generate response using Groq API."""
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY not configured")
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
    )
    
    data = response.json()
    
    # Debug: Print response if there's an error
    if "error" in data:
        print(f"Groq API Error: {data['error']}")
        raise ValueError(f"Groq API error: {data['error']}")
    
    if "choices" not in data:
        print(f"Unexpected Groq response: {data}")
        raise ValueError(f"Unexpected API response: {data}")
    
    return data["choices"][0]["message"]["content"]


def get_llm_response(system_prompt: str, user_prompt: str, response_format: dict = None) -> str:
    """Get an LLM response using Groq API with system and user prompts."""
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY not configured")
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    
    # Add response format if specified (for JSON responses)
    if response_format and response_format.get("type") == "json_object":
        payload["response_format"] = {"type": "json_object"}
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json=payload
    )
    
    data = response.json()
    
    # Debug: Print response if there's an error
    if "error" in data:
        print(f"Groq API Error: {data['error']}")
        raise ValueError(f"Groq API error: {data['error']}")
    
    if "choices" not in data:
        print(f"Unexpected Groq response: {data}")
        raise ValueError(f"Unexpected API response: {data}")
    
    return data["choices"][0]["message"]["content"]