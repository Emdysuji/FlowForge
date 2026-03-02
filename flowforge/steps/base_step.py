"""Base step contract for FlowForge plugins."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseStep(ABC):
    """Abstract base class implemented by all workflow steps."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.validate_config()

    @abstractmethod
    def validate_config(self) -> None:
        """Validate step configuration before execution."""

    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute a step and return output data for next step."""
