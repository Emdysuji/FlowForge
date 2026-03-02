"""Application-level shared dependencies."""
from flowforge.services.scheduler_service import SchedulerService

scheduler_service = SchedulerService()


def get_scheduler() -> SchedulerService:
    return scheduler_service
