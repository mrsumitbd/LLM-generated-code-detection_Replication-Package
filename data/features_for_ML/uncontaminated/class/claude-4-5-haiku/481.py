from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from croniter import croniter


class WorkflowScheduler:
    """Workflow scheduler."""

    def __init__(self, session: AsyncSession, workflow_manager: WorkflowManager):
        self.session = session
        self.workflow_manager = workflow_manager

    def _get_next_run(self, schedule_type: str, schedule_expr: str) -> Optional[datetime]:
        """
        Calculate the next run time based on schedule type and expression.
        
        Args:
            schedule_type: Type of schedule ('cron', 'interval', 'once')
            schedule_expr: Schedule expression (cron string, interval in seconds, or ISO datetime)
        
        Returns:
            Next run datetime or None if invalid
        """
        try:
            if schedule_type == 'cron':
                cron = croniter(schedule_expr, datetime.now())
                return cron.get_next(datetime)
            
            elif schedule_type == 'interval':
                interval_seconds = int(schedule_expr)
                return datetime.now() + timedelta(seconds=interval_seconds)
            
            elif schedule_type == 'once':
                return datetime.fromisoformat(schedule_expr)
            
            else:
                return None
        
        except (ValueError, KeyError, TypeError):
            return None