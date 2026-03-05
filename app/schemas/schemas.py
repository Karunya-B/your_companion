from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Task Schemas ---
class TaskBase(BaseModel):
    description: str
    cognitive_load: str = Field(description="High, Medium, Low, or Recovery")

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    user_id: int
    is_completed: bool
    created_at: datetime
    
    model_config = {"from_attributes": True}

# --- DailyLog Schemas ---
class DailyLogBase(BaseModel):
    sleep_hours: float
    energy_level: int = Field(ge=1, le=10)
    mood: str
    exercise_minutes: int = 0

class DailyLogCreate(DailyLogBase):
    pass

class DailyLogResponse(DailyLogBase):
    id: int
    user_id: int
    date: datetime
    
    model_config = {"from_attributes": True}

# --- ScreenTime Schemas ---
class ScreenTimeBase(BaseModel):
    app_name: str
    duration_minutes: int

class ScreenTimeCreate(ScreenTimeBase):
    pass

class ScreenTimeResponse(ScreenTimeBase):
    id: int
    user_id: int
    date: datetime
    
    model_config = {"from_attributes": True}

# --- Reflection Schemas ---
class ReflectionBase(BaseModel):
    content: str

class ReflectionCreate(ReflectionBase):
    pass

class ReflectionResponse(ReflectionBase):
    id: int
    user_id: int
    date: datetime
    ai_feedback: Optional[str] = None
    
    model_config = {"from_attributes": True}

# --- UserMemory Schemas ---
class UserMemoryResponse(BaseModel):
    focus_duration_pref: int
    burnout_triggers: str
    stress_patterns: str
    learning_rhythm: str
    last_updated: datetime
    
    model_config = {"from_attributes": True}

# --- User Schemas ---
class UserResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    memory: Optional[UserMemoryResponse] = None
    
    model_config = {"from_attributes": True}

# --- Service/Endpoint specific schemas ---
class GuidanceTask(BaseModel):
    description: str
    cognitive_load: str = "Medium"

class DailyGuidanceResponse(BaseModel):
    message: str
    suggested_tasks: list[GuidanceTask] = []
    stress_warning: bool = False

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --- ChatMessage Schemas ---
class ChatMessageBase(BaseModel):
    role: str  # "user" or "ai"
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    user_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class ChatHistoryResponse(BaseModel):
    messages: list[ChatMessageResponse]
