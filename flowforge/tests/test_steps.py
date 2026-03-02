from pathlib import Path

from flowforge.steps.http_request_step import HTTPRequestStep
from flowforge.steps.save_csv_step import SaveCSVStep
from flowforge.steps.transform_step import TransformStep


def test_transform_step_uppercase_and_filter() -> None:
    step = TransformStep(
        {
            "rules": [
                {"action": "uppercase", "field": "name"},
                {"action": "filter_keys", "keys": ["name"]},
            ]
        }
    )
    out = step.execute({"name": "alice", "city": "paris"})
    assert out == {"name": "ALICE"}


def test_save_csv_step(tmp_path: Path) -> None:
    step = SaveCSVStep({"filename": "test.csv", "output_dir": str(tmp_path)})
    out = step.execute({"name": "Alice", "email": "a@example.com"})
    assert Path(out["saved_to"]).exists()


def test_http_request_step(monkeypatch) -> None:
    class DummyResponse:
        status_code = 200

        @staticmethod
        def raise_for_status() -> None:
            return None

        @staticmethod
        def json():
            return {"ok": True}

    def fake_request(*args, **kwargs):
        return DummyResponse()

    monkeypatch.setattr("flowforge.steps.http_request_step.requests.request", fake_request)
    step = HTTPRequestStep({"method": "GET", "url": "https://api.example.com"})
    out = step.execute({"q": "search"})
    assert out["status_code"] == 200
    assert out["body"]["ok"] is True
