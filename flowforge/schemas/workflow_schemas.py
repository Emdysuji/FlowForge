"""Pydantic schemas for workflow APIs."""
from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StepDefinition(BaseModel):
    type: str = Field(..., min_length=1)
    config: dict[str, Any] = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=3)
    schedule: str | None = None
    steps: list[StepDefinition] = Field(..., min_length=1)


class WorkflowResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    schedule: str | None
    steps: list[StepDefinition]
    created_at: datetime


class WorkflowRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    workflow_id: int
    status: str
    input_payload: str | None
    output_payload: str | None
    error_message: str | None
    started_at: datetime
    finished_at: datetime | None


class TriggerWorkflowRequest(BaseModel):
    input_data: dict[str, Any] = Field(default_factory=dict)
