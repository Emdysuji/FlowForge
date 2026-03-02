"""Workflow run API routes."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from flowforge.app.database import get_db
from flowforge.core.workflow_engine import WorkflowEngine
from flowforge.models.workflow import Workflow
from flowforge.models.workflow_run import WorkflowRun
from flowforge.schemas.workflow_schemas import TriggerWorkflowRequest, WorkflowRunResponse

router = APIRouter(tags=["runs"])


@router.post("/workflows/{workflow_id}/run", response_model=WorkflowRunResponse, status_code=status.HTTP_202_ACCEPTED)
def run_workflow(
    workflow_id: int,
    payload: TriggerWorkflowRequest,
    db: Session = Depends(get_db),
) -> WorkflowRunResponse:
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    run = WorkflowEngine(db).run_workflow(workflow, payload.input_data)
    return WorkflowRunResponse.model_validate(run, from_attributes=True)


@router.get("/runs", response_model=list[WorkflowRunResponse])
def list_runs(db: Session = Depends(get_db)) -> list[WorkflowRunResponse]:
    runs = db.query(WorkflowRun).order_by(WorkflowRun.started_at.desc()).all()
    return [WorkflowRunResponse.model_validate(run, from_attributes=True) for run in runs]


@router.get("/runs/{run_id}", response_model=WorkflowRunResponse)
def get_run(run_id: int, db: Session = Depends(get_db)) -> WorkflowRunResponse:
    run = db.get(WorkflowRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return WorkflowRunResponse.model_validate(run, from_attributes=True)
