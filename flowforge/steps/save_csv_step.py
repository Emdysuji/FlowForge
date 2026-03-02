"""CSV persistence step."""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any

from flowforge.app.config import settings
from flowforge.steps.base_step import BaseStep


class SaveCSVStep(BaseStep):
    """Writes list/dict data to a CSV file."""

    def validate_config(self) -> None:
        filename = self.config.get("filename")
        if not filename:
            raise ValueError("SaveCSVStep requires 'filename'")

    def execute(self, input_data: Any) -> dict[str, Any]:
        output_dir = Path(self.config.get("output_dir", settings.csv_output_dir))
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = self.config["filename"]
        if "{timestamp}" in filename:
            filename = filename.replace("{timestamp}", datetime.utcnow().strftime("%Y%m%d%H%M%S"))
        filepath = output_dir / filename

        rows = input_data if isinstance(input_data, list) else [input_data]
        keys: list[str] = []
        for row in rows:
            if isinstance(row, dict):
                for key in row.keys():
                    if key not in keys:
                        keys.append(key)

        with filepath.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys or ["value"])
            writer.writeheader()
            if keys:
                for row in rows:
                    writer.writerow(row if isinstance(row, dict) else {})
            else:
                for row in rows:
                    writer.writerow({"value": str(row)})

        return {"saved_to": str(filepath), "rows": len(rows)}
