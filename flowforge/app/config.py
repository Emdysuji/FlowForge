"""Application configuration for FlowForge."""
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    """Environment-backed settings for FlowForge services."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "FlowForge"
    app_env: str = Field(default="development")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    database_url: str = Field(default="postgresql+psycopg2://flowforge:flowforge@db:5432/flowforge")

    scheduler_timezone: str = Field(default="UTC")

    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_sender: Optional[str] = None
    smtp_use_tls: bool = True

    csv_output_dir: str = Field(default="./data/exports")

    workflow_log_file: str = Field(default="./logs/workflow_runs.log")
    system_log_file: str = Field(default="./logs/system.log")

    requests_timeout_seconds: int = Field(default=20)

    @property
    def base_path(self) -> Path:
        return Path.cwd()


settings = Settings()
