from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()

def create_user(db: Session, name: str = "Karunya"):
    db_user = models.User(name=name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Initialize empty memory
    db_memory = models.UserMemory(user_id=db_user.id)
    db.add(db_memory)
    db.commit()
    return db_user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.model_dump(), user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_for_user(db: Session, user_id: int, completed: bool = False):
    return db.query(models.Task).filter(
        models.Task.user_id == user_id, 
        models.Task.is_completed == completed
    ).all()

def create_daily_log(db: Session, log: schemas.DailyLogCreate, user_id: int):
    db_log = models.DailyLog(**log.model_dump(), user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def create_screen_time(db: Session, screen_time: schemas.ScreenTimeCreate, user_id: int):
    db_screen_time = models.ScreenTime(**screen_time.model_dump(), user_id=user_id)
    db.add(db_screen_time)
    db.commit()
    db.refresh(db_screen_time)
    return db_screen_time

def create_reflection(db: Session, reflection: schemas.ReflectionCreate, user_id: int, ai_feedback: str = None):
    db_reflection = models.Reflection(**reflection.model_dump(), user_id=user_id, ai_feedback=ai_feedback)
    db.add(db_reflection)
    db.commit()
    db.refresh(db_reflection)
    return db_reflection

def update_user_memory(db: Session, user_id: int, memory_updates: dict):
    db_memory = db.query(models.UserMemory).filter(models.UserMemory.user_id == user_id).first()
    if db_memory:
        for key, value in memory_updates.items():
            setattr(db_memory, key, value)
        db.commit()
        db.refresh(db_memory)
    return db_memory

def create_chat_message(db: Session, user_id: int, role: str, content: str):
    """Save a chat message to the database."""
    db_message = models.ChatMessage(user_id=user_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_history(db: Session, user_id: int, limit: int = 100):
    """Retrieve chat history for a user."""
    return db.query(models.ChatMessage).filter(
        models.ChatMessage.user_id == user_id
    ).order_by(models.ChatMessage.created_at.asc()).limit(limit).all()
