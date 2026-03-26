from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# This class stores any settings that the API will use
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

    ALLOWED_ORIGINS: Any = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v # type: ignore
        raise ValueError(v)

    #Builds the full DB URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    #Secret key for JWT tokens
    #Taken from .env
    SECRET_KEY: str = ""

    # All API secrets and keys
    # These are all taken from the .env
    OPENWEATHER_API_KEY: str = ""

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    SENDGRID_API_KEY: str = ""
    SENDGRID_FROM_EMAIL: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()