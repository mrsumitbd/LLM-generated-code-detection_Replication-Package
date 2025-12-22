import asyncio
from typing import Any, Awaitable, Callable, Dict, Optional

class EvaluationRemoteWorkflowHandler:
    """
    Handles the execution of remote evaluation workflows with a configurable
    maximum concurrency. Workflows are expected to be async callables.
    """

    def __init__(self, config: Any, max_concurrency: int):
        """
        :param config: Configuration object for evaluation runs.
        :param max_concurrency: Maximum number of workflows that can run concurrently.
        """
        self.config = config
        self.max_concurrency = max_concurrency
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._tasks: Dict[str, asyncio.Task] = {}
        self._loop = asyncio.get_event_loop()

    async def _run_workflow(
        self,
        workflow_id: str,
        workflow_func: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        async with self._semaphore:
            result = await workflow_func(*args, **kwargs)
            self._tasks[workflow_id] = asyncio.Future()
            self._tasks[workflow_id].set_result(result)
            return result

    def submit_workflow(
        self,
        workflow_id: str,
        workflow_func: Callable[..., Awaitable[Any]],
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
        """
        Submit a workflow for execution. The workflow function must be async.
        """
        task = self._loop.create_task(
            self._run_workflow(workflow_id, workflow_func, *args, **kwargs)
        )
        self._tasks[workflow_id] = task
        return task

    def get_result(self, workflow_id: str) -> Optional[Any]:
        """
        Retrieve the result of a completed workflow. Returns None if the
        workflow is still running or does not exist.
        """
        task = self._tasks.get(workflow_id)
        if task is None:
            return None
        if isinstance(task, asyncio.Task) and task.done():
            return task.result()
        return None

    def cancel_workflow(self, workflow_id: str) -> bool:
        """
        Cancel a running workflow. Returns True if cancellation was requested.
        """
        task = self._tasks.get(workflow_id)
        if isinstance(task, asyncio.Task):
            task.cancel()
            return True
        return False

    def list_workflows(self) -> list[str]:
        """
        Return a list of all workflow IDs currently tracked.
        """
        return list(self._tasks.keys())

    def shutdown(self) -> None:
        """
        Cancel all running workflows and clear internal state.
        """
        for task in self._tasks.values():
            if isinstance(task, asyncio.Task):
                task.cancel()
        self._tasks.clear()