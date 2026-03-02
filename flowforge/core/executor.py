"""Sequential workflow step executor."""
from __future__ import annotations

from typing import Any

from flowforge.core.step_registry import StepRegistry


class WorkflowExecutor:
    """Executes workflow steps in order and passes output between them."""

    def __init__(self, registry: StepRegistry) -> None:
        self.registry = registry

    def execute_steps(self, steps: list[dict[str, Any]], input_data: Any) -> Any:
        current_data = input_data
        for step in steps:
            step_type = step["type"]
            config = step.get("config", {})
            step_instance = self.registry.create(step_type, config)
            current_data = step_instance.execute(current_data)
        return current_data
