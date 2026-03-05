from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Karunya Companion"
    DATABASE_URL: str = "sqlite:///./karunya.db"
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    OLLAMA_URL: str = "http://localhost:11434/api/generate"
    OLLAMA_MODEL: str = "mistral"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
