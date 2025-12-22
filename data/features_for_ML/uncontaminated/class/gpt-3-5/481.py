from datetime import datetime
from typing import Optional
from async_session import AsyncSession
from workflow_manager import WorkflowManager

class WorkflowScheduler:
    """Workflow scheduler."""

    def __init__(self, session: AsyncSession, workflow_manager: WorkflowManager):
        self.session = session
        self.workflow_manager = workflow_manager

    def _get_next_run(self, schedule_type: str, schedule_expr: str) -> Optional[datetime]:
        # Implementation of _get_next_run method goes here
        pass