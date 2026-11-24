from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Apunta al .env en la raíz del monorepo (kairos/.env)
ROOT_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Kairos API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://kairos_dev:kairos_dev_password@localhost:5432/kairos_db"


settings = Settings()