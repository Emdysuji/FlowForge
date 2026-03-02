"""Scheduler service for cron workflow triggers."""
from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from flowforge.app.database import SessionLocal
from flowforge.core.workflow_engine import WorkflowEngine
from flowforge.models.workflow import Workflow


class SchedulerService:
    """Manages APScheduler jobs from persisted workflows."""

    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def schedule_workflow(self, workflow: Workflow) -> None:
        if not workflow.schedule:
            return

        def _runner(workflow_id: int) -> None:
            db = SessionLocal()
            try:
                workflow_instance = db.get(Workflow, workflow_id)
                if workflow_instance:
                    engine = WorkflowEngine(db)
                    engine.run_workflow(workflow_instance, input_data={"trigger": "scheduler"})
            finally:
                db.close()

        self.scheduler.add_job(
            _runner,
            trigger=CronTrigger.from_crontab(workflow.schedule),
            id=f"workflow-{workflow.id}",
            replace_existing=True,
            kwargs={"workflow_id": workflow.id},
        )

    def remove_workflow(self, workflow_id: int) -> None:
        job_id = f"workflow-{workflow_id}"
        if self.scheduler.get_job(job_id):
            self.scheduler.remove_job(job_id)
