import json

from flowforge.core.workflow_engine import WorkflowEngine
from flowforge.models.workflow import Workflow


class FakeDB:
    def __init__(self) -> None:
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def commit(self) -> None:
        return None

    def refresh(self, obj) -> None:
        if getattr(obj, "id", None) is None:
            obj.id = len(self.objects)


def test_workflow_engine_success_path() -> None:
    db = FakeDB()
    workflow = Workflow(
        id=10,
        name="test",
        schedule=None,
        definition_json=json.dumps(
            {
                "steps": [
                    {"type": "transform", "config": {"rules": [{"action": "rename_key", "from": "a", "to": "b"}]}}
                ]
            }
        ),
    )

    run = WorkflowEngine(db).run_workflow(workflow, {"a": "value"})
    assert run.status == "success"
    assert "b" in run.output_payload
