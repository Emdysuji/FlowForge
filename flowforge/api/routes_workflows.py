"""Workflow management API routes."""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from flowforge.app.database import get_db
from flowforge.app.dependencies import get_scheduler
from flowforge.models.workflow import Workflow
from flowforge.schemas.workflow_schemas import WorkflowCreate, WorkflowResponse
from flowforge.services.scheduler_service import SchedulerService

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    payload: WorkflowCreate,
    db: Session = Depends(get_db),
    scheduler: SchedulerService = Depends(get_scheduler),
) -> WorkflowResponse:
    existing = db.query(Workflow).filter(Workflow.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Workflow name already exists")

    workflow = Workflow(name=payload.name, schedule=payload.schedule, definition_json=payload.model_dump_json())
    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    if payload.schedule:
        scheduler.schedule_workflow(workflow)

    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        schedule=workflow.schedule,
        steps=payload.steps,
        created_at=workflow.created_at,
    )


@router.get("", response_model=list[WorkflowResponse])
def list_workflows(db: Session = Depends(get_db)) -> list[WorkflowResponse]:
    workflows = db.query(Workflow).order_by(Workflow.created_at.desc()).all()
    response: list[WorkflowResponse] = []
    for workflow in workflows:
        definition = json.loads(workflow.definition_json)
        response.append(
            WorkflowResponse(
                id=workflow.id,
                name=workflow.name,
                schedule=workflow.schedule,
                steps=definition["steps"],
                created_at=workflow.created_at,
            )
        )
    return response


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: int, db: Session = Depends(get_db)) -> WorkflowResponse:
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    definition = json.loads(workflow.definition_json)
    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        schedule=workflow.schedule,
        steps=definition["steps"],
        created_at=workflow.created_at,
    )


@router.delete("/{workflow_id}", status_code=status.HTTP_200_OK)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    scheduler: SchedulerService = Depends(get_scheduler),
) -> Response:
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    db.delete(workflow)
    db.commit()
    scheduler.remove_workflow(workflow_id)
    return Response(status_code=status.HTTP_200_OK)
