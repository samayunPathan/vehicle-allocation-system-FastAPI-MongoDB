from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MONGODB_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "vehicle_allocation_db"
    
    class Config:
        env_file = ".env"

settings = Settings()