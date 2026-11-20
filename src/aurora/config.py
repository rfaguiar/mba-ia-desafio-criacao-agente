from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    google_api_key: str | None = Field(default=None, validation_alias="GOOGLE_API_KEY")
    gemini_model: str = Field(
        default="gemini-3.1-flash-lite",
        validation_alias="GEMINI_MODEL",
    )
    database_url: str = Field(
        default="sqlite+aiosqlite:///./.data/aurora.db",
        validation_alias="DATABASE_URL",
    )
    seed_directory: Path = Field(default=Path("dados"), validation_alias="SEED_DIRECTORY")
    host: str = Field(default="0.0.0.0", validation_alias="HOST")
    port: int = Field(default=8000, validation_alias="PORT")

    def require_google_api_key(self) -> str:
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY é obrigatória para executar o agente")
        return self.google_api_key


settings = Settings()

