# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Status Page API"
    API_V1_STR: str = "/api/v1"
    
    # Database settings
    SQLALCHEMY_DATABASE_URI: str
    AUTH0_DOMAIN: str
    API_AUDIENCE: str
    DEV_MODE: bool = False
    TEST_TOKEN: Optional[str] = None

    # WebSocket settings
    WEBSOCKET_PORT: int = 5001
    WEBSOCKET_HOST: str = "localhost"
    
    # Email settings
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: str = "your-email@gmail.com"
    MAIL_PASSWORD: str = "your-app-specific-password"
    MAIL_DEFAULT_SENDER: str = "your-email@gmail.com"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "allow"

settings = Settings()

