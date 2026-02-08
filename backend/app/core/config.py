from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path
#from typing import Optional

class Settings(BaseSettings):
    #App Settings
    PROJECT_NAME: str = "MyAPI"
    API_STR: str = "/api/v1"

    #Database Settings
    #Taken from .env
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = ""

    #Builds the full DB URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    #Secret key for JWT tokens
    #Taken from .env
    SECRET_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()