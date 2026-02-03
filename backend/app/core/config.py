from pydantic_settings import BaseSettings
#from typing import Optional

class Settings(BaseSettings):
    #App Settings
    PROJECT_NAME: str = "MyAPI"
    API_STR: str = "/api/v1"

    #Database Settings
    #Taken from .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str = "localhost"

    #Builds the full DB URL
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
    
    #Secret key for JWT tokens
    #Taken from .env
    SECRET_KEY: str

    class Config:
        #Tells pydantic to look for a .env file
        env_file = ".env"

settings = Settings()