from flowforge.core.step_registry import StepRegistry
from flowforge.steps.base_step import BaseStep


class DummyStep(BaseStep):
    def validate_config(self) -> None:
        pass

    def execute(self, input_data):
        return {"ok": True, "input": input_data}


def test_registry_register_and_create() -> None:
    registry = StepRegistry()
    registry.register("dummy", DummyStep)

    step = registry.create("dummy", {})
    assert step.execute({"x": 1})["ok"] is True
    assert "dummy" in registry.available_steps()
