import asyncio
from datetime import datetime
from concurrent.futures import Future
from typing import AsyncIterator, Callable, Dict, List, Optional
from derisk.core.interface.parameter import BaseDeployModelParameters
from derisk.model.parameter import ModelWorkerParameters
from derisk.model.cluster.worker_base import ModelWorker

class WorkerRunData:
    host: str
    port: int
    worker_type: str
    worker_key: str
    worker: ModelWorker
    worker_params: ModelWorkerParameters
    model_params: BaseDeployModelParameters
    stop_event: asyncio.Event
    semaphore: asyncio.Semaphore = None
    command_args: List[str] = None
    _heartbeat_future: Optional[Future] = None
    _last_heartbeat: Optional[datetime] = None
    # Remove from the registry, Just for stop worker
    remove_from_registry: bool = False

    def _to_print_key(self):
        model_name = self.model_params.name
        provider = self.model_params.provider
        host = self.host
        port = self.port
        return f"model {model_name}@{provider}({host}:{port})"

    @property
    def stopped(self):
        """Check if the worker is stopped""" ""
        return self.stop_event.is_set()