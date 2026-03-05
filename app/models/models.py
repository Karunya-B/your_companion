from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="User")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="user")
    logs = relationship("DailyLog", back_populates="user")
    screen_times = relationship("ScreenTime", back_populates="user")
    reflections = relationship("Reflection", back_populates="user")
    memory = relationship("UserMemory", back_populates="user", uselist=False)
    chat_messages = relationship("ChatMessage", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String, index=True)
    cognitive_load = Column(String)  # High, Medium, Low, Recovery
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    sleep_hours = Column(Float)
    energy_level = Column(Integer)  # 1 to 10
    mood = Column(String)
    exercise_minutes = Column(Integer, default=0)

    user = relationship("User", back_populates="logs")

class ScreenTime(Base):
    __tablename__ = "screen_times"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    app_name = Column(String)
    duration_minutes = Column(Integer)

    user = relationship("User", back_populates="screen_times")

class Reflection(Base):
    __tablename__ = "reflections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text)
    ai_feedback = Column(Text, nullable=True)

    user = relationship("User", back_populates="reflections")

class UserMemory(Base):
    __tablename__ = "user_memory"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    focus_duration_pref = Column(Integer, default=60) # mins
    burnout_triggers = Column(Text, default="None identified yet.")
    stress_patterns = Column(Text, default="None identified yet.")
    learning_rhythm = Column(Text, default="Steady paced.")
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="memory")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String)  # "user" or "ai"
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="chat_messages")
