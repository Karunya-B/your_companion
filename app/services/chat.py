from app.services.llm import get_llm_response

def get_system_prompt(user_name: str = "User") -> str:
    """Generate a dynamic system prompt based on the user's name."""
    return f"""You are {user_name}'s study planner and accountability buddy.

## CURRENT USER DATA
{{user_state}}

## YOUR MODES

### MODE 1: PLANNING (when {user_name} says what they want to study)
- Create a full study plan immediately using their available time and energy
- Don't ask endless questions - use the data you have
- Show time blocks, tasks, and WHY each task matters for their goal

### MODE 2: COMPLETION (when {user_name} says "done", "finished", "completed", "okay done", "that's it")
- 🎉 CELEBRATE their work! Be genuinely encouraging
- Ask 1 simple question: "What was hardest about today?" or "How do you feel about the progress?"
- Suggest a reward or reflection
- Offer to log their progress if they want
- DON'T ask them to create a new plan yet
- DON'T suggest more tasks

### MODE 3: REFLECTION (optional)
- If they want to discuss what went well or what was hard
- Listen and encourage
- Then ask: "Want to adjust tomorrow's plan?" or "Ready for a break?"

## RECOGNITION SIGNALS
- "done", "finished", "completed", "ok done", "that's it", "i completed", "all done" = COMPLETION MODE
- "job prep", "linked list", "dsa", "want to study", "let's do" = PLANNING MODE
- "my goal is", "want to", "today i" = PLANNING MODE

## COMPLETION MODE RESPONSE
When user says they're done:
🎉 "Great job completing your tasks today, {user_name}!"
💪 "What was the hardest part for you?"
🎁 "You earned a reward: [suggest one]"
❓ "Want to reflect on what went well?"

## NEVER DO THIS
- Ask "what do you want to study" if they just said "done"
- Repeat the same question twice in one conversation
- Ignore context from earlier messages
- Create a plan without using their energy/time data
- Suggest tasks they didn't mention

## REWARD IDEAS
Coffee break, short walk, watch a video, call a friend, snack, stretch, 20-min game, take a nap
"""




def get_chat_response(user_message: str, user_state: dict) -> str:
    """Generates a planning-assistant response using the user's current state."""
    
    user_name = user_state.get("user_name", "User")
    system_prompt = get_system_prompt(user_name)
    
    state_lines = []
    
    # Memory / profile
    memory = user_state.get("memory", {})
    if memory:
        state_lines.append(f"Focus preference: {memory.get('focus_duration_pref', 60)} minutes")
        state_lines.append(f"Known burnout triggers: {memory.get('burnout_triggers', 'None identified')}")
        state_lines.append(f"Learning rhythm: {memory.get('learning_rhythm', 'Steady')}")
        state_lines.append(f"Stress patterns: {memory.get('stress_patterns', 'None identified')}")

    # Recent health logs
    recent_logs = user_state.get("recent_logs", [])
    if recent_logs:
        latest = recent_logs[0]
        state_lines.append(f"Last logged sleep: {latest.get('sleep_hours', '?')} hours")
        state_lines.append(f"Last energy level: {latest.get('energy_level', '?')}/10")
        state_lines.append(f"Last mood: {latest.get('mood', 'unknown')}")
        state_lines.append(f"Last exercise: {latest.get('exercise_minutes', 0)} minutes")
    else:
        state_lines.append("No recent health logs available.")

    # Screen time
    screen_time = user_state.get("screen_time", [])
    if screen_time:
        total_mins = sum(s.get("duration_minutes", 0) for s in screen_time)
        apps = ", ".join(f"{s['app_name']} ({s['duration_minutes']}m)" for s in screen_time[:5])
        state_lines.append(f"Recent screen time: {total_mins} minutes total — {apps}")
    else:
        state_lines.append("No screen time data logged recently.")

    # Recent reflections
    reflections = user_state.get("recent_reflections", [])
    if reflections:
        state_lines.append(f"Latest reflection: \"{reflections[0][:200]}\"")

    # Pending tasks
    pending = user_state.get("pending_tasks", [])
    if pending:
        task_list = ", ".join(f"{t['description']} ({t['cognitive_load']})" for t in pending[:5])
        state_lines.append(f"Pending tasks: {task_list}")

    # RECENT CHAT HISTORY - This is what was missing!
    recent_chat = user_state.get("recent_chat", [])
    if recent_chat:
        state_lines.append("Recent conversation:")
        for chat in recent_chat[-6:]:  # Last 6 messages (3 exchanges)
            role = "You" if chat["role"] == "user" else "AI"
            content = chat["content"][:100] + "..." if len(chat["content"]) > 100 else chat["content"]
            state_lines.append(f"  {role}: {content}")

    user_state_text = "\n".join(state_lines) if state_lines else "No user data available yet."
    
    prompt = system_prompt.replace("{user_state}", user_state_text)
    
    response = get_llm_response(system_prompt=prompt, user_prompt=user_message)
    
    if not response:
        return f"{user_name}, let's start with a simple plan: Solve 2 linked list problems (45 minutes), take a short break, then watch your OOP lecture."
        
    return response
