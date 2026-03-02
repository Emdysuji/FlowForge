"""Structured logging setup."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from flowforge.app.config import settings


class JsonFormatter(logging.Formatter):
    """Simple JSON formatter for structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "workflow_id"):
            payload["workflow_id"] = record.workflow_id
        if hasattr(record, "run_id"):
            payload["run_id"] = record.run_id
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def _build_file_handler(path: str) -> logging.Handler:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(path)
    handler.setFormatter(JsonFormatter())
    return handler


def configure_logging() -> None:
    """Configure application loggers with separate files."""
    system_logger = logging.getLogger("flowforge.system")
    run_logger = logging.getLogger("flowforge.runs")

    system_logger.setLevel(logging.INFO)
    run_logger.setLevel(logging.INFO)

    if not system_logger.handlers:
        system_logger.addHandler(_build_file_handler(settings.system_log_file))
    if not run_logger.handlers:
        run_logger.addHandler(_build_file_handler(settings.workflow_log_file))
