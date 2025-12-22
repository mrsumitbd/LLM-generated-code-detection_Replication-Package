from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional

try:
    from croniter import croniter
except ImportError:  # pragma: no cover
    croniter = None

# Assume these are defined elsewhere in the project
try:
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:  # pragma: no cover
    AsyncSession = object  # type: ignore

try:
    from .workflow_manager import WorkflowManager
except Exception:  # pragma: no cover
    WorkflowManager = object  # type: ignore


class WorkflowScheduler:
    """Workflow scheduler."""

    def __init__(self, session: AsyncSession, workflow_manager: WorkflowManager):
        """
        Initialize the scheduler with an async database session and a workflow manager.

        :param session: AsyncSession for database interactions.
        :param workflow_manager: Instance responsible for workflow lifecycle.
        """
        self.session = session
        self.workflow_manager = workflow_manager

    def _get_next_run(self, schedule_type: str, schedule_expr: str) -> Optional[datetime]:
        """
        Compute the next run time for a workflow based on its schedule type and expression.

        Supported schedule types:
            - 'cron':   schedule_expr is a cron string (e.g., '*/5 * * * *')
            - 'interval': schedule_expr is a relative interval like '5m', '2h', '1d'
            - 'date':   schedule_expr is an ISO‑8601 datetime string

        :param schedule_type: The type of schedule.
        :param schedule_expr: The schedule expression.
        :return: The next datetime to run the workflow, or None if it cannot be parsed.
        """
        now = datetime.utcnow()

        if schedule_type == "cron":
            if croniter is None:
                return None
            try:
                itr = croniter(schedule_expr, now)
                return itr.get_next(datetime)
            except Exception:
                return None

        if schedule_type == "interval":
            # Expected format: <number><unit>, e.g., 5m, 2h, 1d
            match = re.fullmatch(r"(\d+)([smhd])", schedule_expr.strip())
            if not match:
                return None
            value, unit = match.groups()
            value = int(value)
            if unit == "s":
                delta = timedelta(seconds=value)
            elif unit == "m":
                delta = timedelta(minutes=value)
            elif unit == "h":
                delta = timedelta(hours=value)
            elif unit == "d":
                delta = timedelta(days=value)
            else:
                return None
            return now + delta

        if schedule_type == "date":
            try:
                target = datetime.fromisoformat(schedule_expr)
                # If the parsed time is in the past, return None
                return target if target > now else None
            except Exception:
                return None

        # Unsupported schedule type
        return None