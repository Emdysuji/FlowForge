"""HTTP request step."""
from __future__ import annotations

from typing import Any

import requests

from flowforge.app.config import settings
from flowforge.steps.base_step import BaseStep


class HTTPRequestStep(BaseStep):
    """Calls external APIs using GET/POST."""

    def validate_config(self) -> None:
        if "url" not in self.config:
            raise ValueError("HTTPRequestStep requires 'url'")
        method = self.config.get("method", "GET").upper()
        if method not in {"GET", "POST"}:
            raise ValueError("HTTPRequestStep supports GET/POST only")

    def execute(self, input_data: Any) -> dict[str, Any]:
        method = self.config.get("method", "GET").upper()
        headers = self.config.get("headers", {})
        payload = self.config.get("payload", input_data)
        response = requests.request(
            method,
            self.config["url"],
            headers=headers,
            json=payload if method == "POST" else None,
            params=payload if method == "GET" and isinstance(payload, dict) else None,
            timeout=settings.requests_timeout_seconds,
        )
        response.raise_for_status()
        body: Any
        try:
            body = response.json()
        except ValueError:
            body = response.text
        return {"status_code": response.status_code, "body": body}
