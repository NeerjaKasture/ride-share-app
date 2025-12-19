from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

# Load .env file from project root
load_dotenv(dotenv_path=os.path.join(
    os.path.dirname(__file__), '..', '..', '.env'))


class Settings(BaseSettings):
    POSTGRES: str
    SECRET_KEY: str
    ALGORITHM: str
    POSTGRES_SYNC: str

    model_config = SettingsConfigDict(
        env_file="../../.env",
        extra="ignore"
    )


settings = Settings()  # type: ignore
