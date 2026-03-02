"""Dynamic step registration and resolution."""
from __future__ import annotations

from typing import Type

from flowforge.steps.base_step import BaseStep


class StepRegistry:
    """Registry for mapping step type identifiers to classes."""

    def __init__(self) -> None:
        self._registry: dict[str, Type[BaseStep]] = {}

    def register(self, step_type: str, step_cls: Type[BaseStep]) -> None:
        if not issubclass(step_cls, BaseStep):
            raise TypeError("step_cls must subclass BaseStep")
        self._registry[step_type] = step_cls

    def create(self, step_type: str, config: dict) -> BaseStep:
        step_cls = self._registry.get(step_type)
        if step_cls is None:
            raise ValueError(f"Unregistered step type: {step_type}")
        return step_cls(config)

    def available_steps(self) -> list[str]:
        return sorted(self._registry.keys())
