from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas import schemas
from app.crud import crud
from app.services import tasks_flow, guidance, analyzer, chat

router = APIRouter(prefix="/api/v1", tags=["Companion"])

DbDep = Annotated[Session, Depends(get_db)]

def get_current_user_id(db: DbDep) -> int:
    # MVP: Just use the first user or create one if it doesn't exist
    user = db.query(crud.models.User).first()
    if not user:
        user = crud.create_user(db)
    return user.id

UserIdDep = Annotated[int, Depends(get_current_user_id)]

@router.post("/log_daily_tasks", response_model=list[schemas.TaskResponse])
async def log_daily_tasks(tasks: list[str], db: DbDep, user_id: UserIdDep):
    # Get flow from AI
    flow = tasks_flow.generate_task_flow(tasks)
    
    responses = []
    for item in flow:
        task_create = schemas.TaskCreate(description=item.get("description", ""), cognitive_load=item.get("cognitive_load", "Medium"))
        db_task = crud.create_task(db=db, task=task_create, user_id=user_id)
        responses.append(db_task)
    return responses

@router.post("/log_sleep_data", response_model=schemas.DailyLogResponse)
async def log_sleep_data(log: schemas.DailyLogCreate, db: DbDep, user_id: UserIdDep):
    return crud.create_daily_log(db=db, log=log, user_id=user_id)

@router.post("/log_screen_time", response_model=schemas.ScreenTimeResponse)
async def log_screen_time(screen_time: schemas.ScreenTimeCreate, db: DbDep, user_id: UserIdDep):
    return crud.create_screen_time(db=db, screen_time=screen_time, user_id=user_id)

@router.post("/log_reflection", response_model=schemas.ReflectionResponse)
async def log_reflection(reflection: schemas.ReflectionCreate, db: DbDep, user_id: UserIdDep):
    # Fetch current memory
    user = crud.get_user(db, user_id)
    memory_dict = {
        "focus_duration_pref": user.memory.focus_duration_pref,
        "burnout_triggers": user.memory.burnout_triggers,
        "stress_patterns": user.memory.stress_patterns,
        "learning_rhythm": user.memory.learning_rhythm
    } if user.memory else {}
    
    # Analyze reflection
    analysis = analyzer.analyze_reflection(reflection.content, memory_dict)
    
    # Update memory if needed
    if analysis.get("memory_updates"):
        crud.update_user_memory(db, user_id, analysis["memory_updates"])
        
    return crud.create_reflection(db=db, reflection=reflection, user_id=user_id, ai_feedback=analysis.get("feedback"))

@router.get("/generate_daily_guidance", response_model=schemas.DailyGuidanceResponse)
async def generate_daily_guidance(db: DbDep, user_id: UserIdDep):
    try:
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        memory_dict = {
            "focus_duration_pref": user.memory.focus_duration_pref,
            "burnout_triggers": user.memory.burnout_triggers,
            "stress_patterns": user.memory.stress_patterns,
            "learning_rhythm": user.memory.learning_rhythm
        } if user.memory else {}
        
        # Get today's logs (MVP: just get the latest logs)
        logs = db.query(crud.models.DailyLog).filter(crud.models.DailyLog.user_id == user_id).order_by(crud.models.DailyLog.date.desc()).limit(3).all()
        logs_data = [{"sleep_hours": l.sleep_hours, "energy_level": l.energy_level, "mood": l.mood} for l in logs]
        
        # Get uncompleted tasks
        tasks = crud.get_tasks_for_user(db, user_id, completed=False)
        tasks_data = [{"description": t.description, "cognitive_load": t.cognitive_load} for t in tasks]
        
        guidance_data = guidance.evaluate_daily_guidance(memory_dict, logs_data, tasks_data)
        
        return schemas.DailyGuidanceResponse(**guidance_data)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Guidance error: {e}")
        return schemas.DailyGuidanceResponse(
            message="Good morning! I'm having trouble generating guidance right now. Take it easy today!",
            suggested_tasks=[],
            stress_warning=False,
        )

@router.post("/chat", response_model=schemas.ChatResponse)
async def chat_interaction(chat_req: schemas.ChatRequest, db: DbDep, user_id: UserIdDep):
    try:
        user = crud.get_user(db, user_id)
        
        # -- Build rich user state from the database --
        user_state = {}
        
        # User info
        user_state["user_name"] = user.name if user else "User"
        
        # Memory / profile
        if user and user.memory:
            user_state["memory"] = {
                "focus_duration_pref": user.memory.focus_duration_pref,
                "burnout_triggers": user.memory.burnout_triggers,
                "stress_patterns": user.memory.stress_patterns,
                "learning_rhythm": user.memory.learning_rhythm,
            }
        
        # Recent health logs (last 3)
        logs = db.query(crud.models.DailyLog).filter(
            crud.models.DailyLog.user_id == user_id
        ).order_by(crud.models.DailyLog.date.desc()).limit(3).all()
        user_state["recent_logs"] = [
            {"sleep_hours": l.sleep_hours, "energy_level": l.energy_level,
             "mood": l.mood, "exercise_minutes": l.exercise_minutes}
            for l in logs
        ]
        
        # Recent screen time (last 5 entries)
        screens = db.query(crud.models.ScreenTime).filter(
            crud.models.ScreenTime.user_id == user_id
        ).order_by(crud.models.ScreenTime.date.desc()).limit(5).all()
        user_state["screen_time"] = [
            {"app_name": s.app_name, "duration_minutes": s.duration_minutes}
            for s in screens
        ]
        
        # Latest reflections (last 2)
        refs = db.query(crud.models.Reflection).filter(
            crud.models.Reflection.user_id == user_id
        ).order_by(crud.models.Reflection.date.desc()).limit(2).all()
        user_state["recent_reflections"] = [r.content for r in refs]
        
        # Pending tasks
        tasks = crud.get_tasks_for_user(db, user_id, completed=False)
        user_state["pending_tasks"] = [
            {"description": t.description, "cognitive_load": t.cognitive_load}
            for t in tasks
        ]
        
        # Recent chat history (last 10 messages for context)
        chat_history = crud.get_chat_history(db, user_id, limit=10)
        user_state["recent_chat"] = [
            {"role": msg.role, "content": msg.content}
            for msg in chat_history
        ]
        
        # Save the user message first
        crud.create_chat_message(db=db, user_id=user_id, role="user", content=chat_req.message)
        
        reply = chat.get_chat_response(chat_req.message, user_state)
        if not reply:
            reply = "Sorry, I couldn't process that. Please try again."
        
        # Save the AI response
        crud.create_chat_message(db=db, user_id=user_id, role="assistant", content=reply)
        
        return schemas.ChatResponse(reply=reply)
    except Exception as e:
        print(f"Chat error: {e}")
        return schemas.ChatResponse(reply="Sorry, something went wrong. Please try again.")

@router.post("/chat/save", response_model=schemas.ChatMessageResponse)
async def save_chat_message(message: schemas.ChatMessageCreate, db: DbDep, user_id: UserIdDep):
    """Save a chat message to history."""
    return crud.create_chat_message(db=db, user_id=user_id, role=message.role, content=message.content)

@router.get("/chat/history", response_model=schemas.ChatHistoryResponse)
async def get_chat_history(db: DbDep, user_id: UserIdDep):
    """Retrieve chat history for the user."""
    messages = crud.get_chat_history(db=db, user_id=user_id)
    return schemas.ChatHistoryResponse(messages=messages)

@router.delete("/reset")
async def reset_data(db: DbDep, user_id: UserIdDep):
    """Reset all user data (tasks, logs, etc.) for testing."""
    # Delete all tasks
    db.query(crud.models.Task).filter(crud.models.Task.user_id == user_id).delete()
    # Delete all logs
    db.query(crud.models.DailyLog).filter(crud.models.DailyLog.user_id == user_id).delete()
    # Delete all screen time
    db.query(crud.models.ScreenTime).filter(crud.models.ScreenTime.user_id == user_id).delete()
    # Delete all reflections
    db.query(crud.models.Reflection).filter(crud.models.Reflection.user_id == user_id).delete()
    # Delete chat messages
    db.query(crud.models.ChatMessage).filter(crud.models.ChatMessage.user_id == user_id).delete()
    
    db.commit()
    return {"message": "All user data reset successfully"}
