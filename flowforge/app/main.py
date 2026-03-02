"""FlowForge FastAPI entrypoint."""
from __future__ import annotations

import json
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from flowforge.api.routes_runs import router as runs_router
from flowforge.api.routes_workflows import router as workflows_router
from flowforge.app.config import settings
from flowforge.app.database import Base, SessionLocal, engine, get_db
from flowforge.app.dependencies import scheduler_service
from flowforge.models.workflow import Workflow
from flowforge.models.workflow_run import WorkflowRun
from flowforge.services.logging_service import configure_logging

configure_logging()
logger = logging.getLogger("flowforge.system")

app = FastAPI(title=settings.app_name)
app.include_router(workflows_router)
app.include_router(runs_router)
templates = Jinja2Templates(directory="flowforge/templates")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    scheduler_service.start()
    db = SessionLocal()
    try:
        workflows = db.query(Workflow).filter(Workflow.schedule.is_not(None)).all()
        for workflow in workflows:
            scheduler_service.schedule_workflow(workflow)
    finally:
        db.close()
    logger.info("FlowForge startup complete")


@app.on_event("shutdown")
def on_shutdown() -> None:
    scheduler_service.shutdown()
    logger.info("FlowForge shutdown complete")


@app.get("/dashboard", response_class=HTMLResponse, tags=["dashboard"])
def dashboard(request: Request, db: Session = Depends(get_db)) -> HTMLResponse:
    workflows = db.query(Workflow).order_by(Workflow.created_at.desc()).all()
    runs = db.query(WorkflowRun).order_by(WorkflowRun.started_at.desc()).limit(50).all()
    workflow_view = [
        {
            "id": wf.id,
            "name": wf.name,
            "schedule": wf.schedule or "manual",
            "steps": len(json.loads(wf.definition_json).get("steps", [])),
        }
        for wf in workflows
    ]
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "workflows": workflow_view, "runs": runs},
    )


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}
