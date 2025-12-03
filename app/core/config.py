from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    COHERE_API_KEY: str
    EMBEDDING_MODEL: str = "embed-english-v3.0"
    DB_FILE: str = "default_db.jsonl"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    @field_validator("DB_FILE", mode="before")
    @classmethod
    def ensure_jsonl_extension(cls, v: str) -> str:
        """Ensure DB_FILE always has .jsonl extension."""
        if not v.endswith(".jsonl"):
            if "." in v:
                v = v.rsplit(".", 1)[0]
            return f"{v}.jsonl"
        return v


def get_settings() -> Settings:
    return Settings()
