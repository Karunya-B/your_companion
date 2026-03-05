import json
from app.services.llm import get_llm_response

def analyze_reflection(reflection_text: str, current_memory: dict) -> dict:
    """Uses the LLM to analyze the daily reflection and extract memory updates and feedback."""
    system_prompt = """You are a supportive personal AI mentor.
Your job is to read the user's daily reflection and provide two things:
1. 'feedback': A short, empathetic, supportive response acknowledging their effort and feelings. It should not be a task list, just a thoughtful friend.
2. 'memory_updates': If the reflection reveals any new information about their focus duration preferences, burnout triggers, learning rhythms, or stress patterns, extract them. If nothing new, return empty strings for those fields.

Output in JSON format with the keys 'feedback' and 'memory_updates'. The 'memory_updates' should be an object with keys: 'focus_duration_pref' (int), 'burnout_triggers' (str), 'stress_patterns' (str), 'learning_rhythm' (str). ONLY output valid JSON.
"""
    
    user_prompt = f"Current Memory:\n{json.dumps(current_memory, indent=2)}\n\nUser Reflection:\n{reflection_text}"
    
    response = get_llm_response(
        system_prompt=system_prompt, 
        user_prompt=user_prompt,
        response_format={"type": "json_object"}
    )
    
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"feedback": "Thank you for reflecting today. I'm here to support you.", "memory_updates": {}}
