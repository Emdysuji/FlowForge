"""Workflow ORM model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flowforge.app.database import Base


class Workflow(Base):
    """Persisted workflow definition and schedule."""

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    schedule: Mapped[str | None] = mapped_column(String(100), nullable=True)
    definition_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    runs = relationship("WorkflowRun", back_populates="workflow", cascade="all,delete")
