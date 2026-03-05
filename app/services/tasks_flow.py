import json
from app.services.llm import get_llm_response

def generate_task_flow(tasks: list[str]) -> list[dict]:
    """Sorts and classifies user tasks into a balanced flow."""
    system_prompt = """You are an AI life orchestrator. The user has provided a list of tasks they want to do today.
Your goal is to classify them by cognitive load: 'High', 'Medium', 'Low', or 'Recovery'.
Then, output the tasks in a balanced sequence to avoid burnout (e.g., Medium -> High -> Recovery -> High -> Low).

Output ONLY a JSON array of objects. Each object must have:
- 'description': (str) The task description.
- 'cognitive_load': (str) 'High', 'Medium', 'Low', or 'Recovery'.
"""
    
    user_prompt = f"Tasks to sequence:\n" + "\n".join(f"- {task}" for task in tasks)
    
    response = get_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format={"type": "json_object"}
    )
    
    # Standardize output format
    try:
        parsed = json.loads(response)
        # Handle cases where LLM wraps it in a root key
        if isinstance(parsed, dict) and len(parsed.keys()) == 1:
            parsed = list(parsed.values())[0]
        return parsed if isinstance(parsed, list) else []
    except Exception:
        return [{"description": t, "cognitive_load": "Medium"} for t in tasks]
