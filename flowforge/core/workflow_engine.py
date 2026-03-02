"""Workflow orchestration service."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from flowforge.core.executor import WorkflowExecutor
from flowforge.core.step_registry import StepRegistry
from flowforge.models.workflow import Workflow
from flowforge.models.workflow_run import WorkflowRun
from flowforge.steps.email_step import EmailStep
from flowforge.steps.http_request_step import HTTPRequestStep
from flowforge.steps.save_csv_step import SaveCSVStep
from flowforge.steps.transform_step import TransformStep
from flowforge.steps.web_scrape_step import WebScrapeStep


class WorkflowEngine:
    """Coordinates workflow execution, persistence, and error handling."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.registry = StepRegistry()
        self.executor = WorkflowExecutor(self.registry)
        self.logger = logging.getLogger("flowforge.runs")
        self._register_default_steps()

    def _register_default_steps(self) -> None:
        self.registry.register("web_scrape", WebScrapeStep)
        self.registry.register("transform", TransformStep)
        self.registry.register("email", EmailStep)
        self.registry.register("save_csv", SaveCSVStep)
        self.registry.register("http_request", HTTPRequestStep)

    def run_workflow(self, workflow: Workflow, input_data: dict[str, Any] | None = None) -> WorkflowRun:
        """Execute one workflow definition and persist run state."""
        run = WorkflowRun(
            workflow_id=workflow.id,
            status="running",
            input_payload=json.dumps(input_data or {}),
            started_at=datetime.utcnow(),
        )
        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        try:
            definition = json.loads(workflow.definition_json)
            output_data = self.executor.execute_steps(definition["steps"], input_data or {})
            run.status = "success"
            run.output_payload = json.dumps(output_data, default=str)
            run.finished_at = datetime.utcnow()
            self.db.commit()
            self.logger.info(
                "workflow completed",
                extra={"workflow_id": workflow.id, "run_id": run.id},
            )
        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)
            run.finished_at = datetime.utcnow()
            self.db.commit()
            self.logger.exception(
                "workflow failed",
                extra={"workflow_id": workflow.id, "run_id": run.id},
            )
        return run
