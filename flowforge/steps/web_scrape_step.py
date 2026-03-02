"""HTML scraping step implementation."""
from __future__ import annotations

from typing import Any

import requests
from bs4 import BeautifulSoup

from flowforge.app.config import settings
from flowforge.steps.base_step import BaseStep


class WebScrapeStep(BaseStep):
    """Fetches a web page and extracts content via CSS selectors."""

    def validate_config(self) -> None:
        if "url" not in self.config:
            raise ValueError("WebScrapeStep requires 'url'")
        if "selectors" not in self.config or not isinstance(self.config["selectors"], dict):
            raise ValueError("WebScrapeStep requires 'selectors' as dict")

    def execute(self, input_data: Any) -> dict[str, Any]:
        response = requests.get(self.config["url"], timeout=settings.requests_timeout_seconds)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        results: dict[str, Any] = {"source": self.config["url"]}
        for key, selector in self.config["selectors"].items():
            elements = soup.select(selector)
            results[key] = [el.get_text(strip=True) for el in elements]

        if input_data:
            results["previous"] = input_data
        return results
