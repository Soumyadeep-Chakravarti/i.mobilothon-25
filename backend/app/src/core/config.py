# backend/app/src/core/config.py
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Core Application Settings
    APP_NAME: str = "V1.3 Backend"
    ENV: str = "local"
    DEBUG: bool = True

    # Database Settings (MongoDB)
    MONGO_URI: str = "mongodb://localhost:27017/v13_db"

    # Cache/Queue Settings (Redis)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security Settings
    JWT_SECRET_KEY: str = "super-secret-key"  # **Rotatable**
    ALGORITHM: str = "HS256"

    # ML/Task Settings
    ML_SERVICE_TIMEOUT_SEC: int = 10
    TASK_MAX_RETRIES: int = 3

    class Config:
        # Load environment variables from a .env file
        env_file = ".env"


settings = Settings()
