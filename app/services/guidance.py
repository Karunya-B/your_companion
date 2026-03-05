from app.services.llm import get_llm_response
import json

def _clean_guidance_response(data: dict, fallback_tasks: list) -> dict:
    """Flattens nested AI outputs and ensures types match the schema."""
    try:
        # 1. Ensure message is a string
        message = data.get("message")
        if isinstance(message, dict):
            message = message.get("message") or message.get("content") or "Have a great day!"
        if not isinstance(message, str):
            message = str(message) if message is not None else "Have a great day!"

        # 2. Ensure stress_warning is a boolean
        stress_warning = data.get("stress_warning", False)
        if not isinstance(stress_warning, bool):
            stress_warning = str(stress_warning).lower() == "true"

        # 3. Clean suggested tasks
        raw_tasks = data.get("suggested_tasks")
        clean_tasks = []
        
        if isinstance(raw_tasks, list):
            for t in raw_tasks:
                if not isinstance(t, dict):
                    continue
                
                # Handle nested description: {"description": {"description": "...", "cognitive_load": "..."}}
                desc = t.get("description", "")
                load = t.get("cognitive_load", "Medium")
                
                if isinstance(desc, dict):
                    # Try to extract from nested object if AI made a mistake
                    inner_desc = desc.get("description") or desc.get("content")
                    inner_load = desc.get("cognitive_load")
                    if inner_desc: desc = inner_desc
                    if inner_load: load = inner_load
                
                if isinstance(load, dict):
                    load = load.get("cognitive_load") or load.get("load") or "Medium"

                clean_tasks.append({
                    "description": str(desc) if desc else "Unknown task",
                    "cognitive_load": str(load) if load else "Medium"
                })

        if not clean_tasks:
             clean_tasks = [{"description": str(t.get("description", t)), "cognitive_load": t.get("cognitive_load", "Medium") if isinstance(t, dict) else "Medium"} for t in fallback_tasks]

        return {
            "message": message,
            "stress_warning": stress_warning,
            "suggested_tasks": clean_tasks
        }
    except Exception as e:
        print(f"Error cleaning guidance: {e}")
        return {
            "message": "Have a great day Karunya!",
            "stress_warning": False,
            "suggested_tasks": [{"description": str(t.get("description", t)), "cognitive_load": "Medium"} for t in fallback_tasks]
        }

def evaluate_daily_guidance(user_memory: dict, today_logs: list, tasks: list) -> dict:
    """Analyzes recent logs and tasks to provide guidance and check for stress/burnout."""
    
    # If no pending tasks, don't suggest any
    if not tasks:
        system_prompt = """You are Karunya Companion, a supportive AI mentor. 
Review the user's current memory and recent logs (sleep, energy, mood, exercise).
Provide a 'message': A short, encouraging message for the day. If they slept poorly or have low energy, suggest taking it easy.
Set 'stress_warning': true if their logs indicate they might be pushing too hard.
Set 'suggested_tasks': [] (empty list) since they have no pending tasks.

Respond ONLY in JSON format:
{
  "message": "Good morning Karunya! You seem a bit tired today, let's keep the tasks light.",
  "stress_warning": true,
  "suggested_tasks": []
}
"""
    else:
        system_prompt = """You are Karunya Companion, a supportive AI mentor. 
Review the user's current memory, their recent logs (sleep, energy, mood, exercise), and today's tasks.
1. Provide a 'message': A short, encouraging message for the day. If they slept poorly or have low energy, suggest taking it easy.
2. Provide a 'stress_warning': A boolean (true/false). Set to true if their logs (low sleep, low mood, high screen time) or memory indicate they might be pushing too hard.
3. Provide 'suggested_tasks': Organize their EXISTING tasks for the day into a balanced flow, categorized by cognitive load (High, Medium, Low, Recovery). DO NOT add new tasks.

Respond ONLY in JSON format:
{
  "message": "Good morning Karunya! You seem a bit tired today, let's keep the tasks light.",
  "stress_warning": true,
  "suggested_tasks": [
    {"description": "Review notes", "cognitive_load": "Low"},
    {"description": "Solve 1 coding problem", "cognitive_load": "High"},
    {"description": "Go for a walk", "cognitive_load": "Recovery"}
  ]
}
"""
    
    user_prompt = f"User Memory:\n{json.dumps(user_memory, indent=2)}\n\nRecent Logs:\n{json.dumps(today_logs, indent=2)}\n\nToday's Tasks:\n{json.dumps(tasks, indent=2)}"
    
    response = get_llm_response(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format={"type": "json_object"}
    )
    
    try:
        data = json.loads(response)
        return _clean_guidance_response(data, tasks)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Guidance parsing error: {e}")
        return _clean_guidance_response({}, tasks)
