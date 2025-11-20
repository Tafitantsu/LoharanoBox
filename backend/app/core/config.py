# import du config depuis .env avec exemple de variable

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Kariera4D Backend"
    VERSION: str = "1.0.0"

    DATABASE_URL: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Super Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    LOG_LEVEL: str = "info"

    # Search weights
    FTS_WEIGHT: float = 1.0
    VECTOR_WEIGHT: float = 0.5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()
