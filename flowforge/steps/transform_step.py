"""Data transformation step implementation."""
from __future__ import annotations

from typing import Any

from flowforge.steps.base_step import BaseStep


class TransformStep(BaseStep):
    """Applies lightweight transformations to dict or list data."""

    def validate_config(self) -> None:
        rules = self.config.get("rules")
        if not isinstance(rules, list) or not rules:
            raise ValueError("TransformStep requires non-empty list 'rules'")

    def execute(self, input_data: Any) -> Any:
        data = input_data
        for rule in self.config["rules"]:
            action = rule.get("action")
            if action == "uppercase" and isinstance(data, dict):
                field = rule.get("field")
                if field in data and isinstance(data[field], str):
                    data[field] = data[field].upper()
            elif action == "rename_key" and isinstance(data, dict):
                old_key = rule.get("from")
                new_key = rule.get("to")
                if old_key in data and new_key:
                    data[new_key] = data.pop(old_key)
            elif action == "filter_keys" and isinstance(data, dict):
                keys = set(rule.get("keys", []))
                data = {k: v for k, v in data.items() if k in keys}
        return data
