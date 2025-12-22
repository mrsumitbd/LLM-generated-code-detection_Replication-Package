import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, Future
from typing import Any, Optional, List


class LiteAvatarWorkerManager:
    """
    Manages a pool of worker processes that run the avatar handler script.
    """

    def __init__(self, concurrent_limit: int, handler_root: str, config: Any):
        """
        :param concurrent_limit: Maximum number of concurrent worker processes.
        :param handler_root: Path to the directory containing the handler script.
        :param config: Configuration object for the TTS‑to‑Face conversion.
        """
        self.concurrent_limit = concurrent_limit
        self.handler_root = os.path.abspath(handler_root)
        self.config = config
        self._executor: Optional[ProcessPoolExecutor] = None
        self._futures: List[Future] = []

    def _worker_entry(self, *args, **kwargs):
        """
        Entry point for each worker process. It simply runs the handler script
        with the provided arguments. The handler script is expected to be
        executable and located in `self.handler_root`.
        """
        script_path = os.path.join(self.handler_root, "handler.py")
        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Handler script not found: {script_path}")

        # Build the command. The handler script should accept arguments
        # that are passed via *args and **kwargs. For simplicity we
        # serialize kwargs as JSON on the command line.
        import json
        cmd = ["python", script_path] + list(args)
        if kwargs:
            cmd.append(json.dumps(kwargs))

        # Execute the script and capture its output
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout

    def start_worker(self, *args, **kwargs) -> Future:
        """
        Submit a new job to the worker pool. The job will run the handler
        script with the supplied arguments.

        :return: A Future representing the asynchronous execution.
        """
        if self._executor is None:
            self._executor = ProcessPoolExecutor(max_workers=self.concurrent_limit)

        future = self._executor.submit(self._worker_entry, *args, **kwargs)
        self._futures.append(future)
        return future

    def destroy(self):
        """
        Shut down the worker pool and wait for all running jobs to finish.
        """
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
        self._futures.clear()