from pymongo import MongoClient
from pymongo.database import Database

# from core.config import settings

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://127.0.0.1:27017"
    mongodb_database: str = "clinical_note_parser"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()


client = MongoClient(
    settings.mongodb_uri,
    serverSelectionTimeoutMS=5000,
)

database: Database = client[settings.mongodb_database]


def verify_database_connection() -> None:
    """Raise an exception if MongoDB cannot be reached."""
    client.admin.command("ping")

verify_database_connection()
print("MongoDB connected")