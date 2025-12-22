import logging
from collections import deque
from typing import Dict, List, Optional

# Basic Service implementation used by the bootstrapper
class Service:
    def __init__(self, name: str, dependencies: Optional[List[str]] = None):
        self.name = name
        self.dependencies = dependencies or []
        self.started = False

    def start(self) -> None:
        """Simulate starting the service."""
        self.started = True

    def __repr__(self) -> str:
        return f"<Service {self.name} started={self.started}>"


class AgentBootstrapper:
    """Handles all agent initialization in proper order.

    This class orchestrates the initialization of all services,
    ensuring dependencies are resolved and services start in
    the correct order.
    """

    def __init__(self) -> None:
        self._services: Dict[str, Service] = {}
        self._init_order: List[str] = []
        self._initialized: bool = False

        # Define services and their dependencies
        self._services["database"] = Service("database")
        self._services["cache"] = Service("cache", dependencies=["database"])
        self._services["auth"] = Service("auth", dependencies=["database"])
        self._services["api"] = Service("api", dependencies=["auth", "cache"])
        self._services["worker"] = Service("worker", dependencies=["api"])

        # Resolve start order
        self._resolve_start_order()

        # Start services
        self._start_services()

        # Log summary
        self._log_initialization_summary()

    def _resolve_start_order(self) -> None:
        """Topologically sort services based on dependencies."""
        indegree: Dict[str, int] = {name: 0 for name in self._services}
        for svc in self._services.values():
            for dep in svc.dependencies:
                indegree[svc.name] += 1

        queue = deque([name for name, deg in indegree.items() if deg == 0])
        order: List[str] = []

        while queue:
            name = queue.popleft()
            order.append(name)
            for svc in self._services.values():
                if name in svc.dependencies:
                    indegree[svc.name] -= 1
                    if indegree[svc.name] == 0:
                        queue.append(svc.name)

        if len(order) != len(self._services):
            raise RuntimeError("Circular dependency detected among services")

        self._init_order = order

    def _start_services(self) -> None:
        """Start services in resolved order."""
        for name in self._init_order:
            svc = self._services[name]
            svc.start()
        self._initialized = True

    def _log_initialization_summary(self) -> None:
        """Log a summary of the initialization process."""
        logger = logging.getLogger(__name__)
        logger.info("Agent initialization summary:")
        for name in self._init_order:
            svc = self._services[name]
            logger.info(f"  - {svc.name}: {'started' if svc.started else 'not started'}")

    def get_service(self, service_name: str) -> Service | None:
        """Return the service instance by name, or None if not found."""
        return self._services.get(service_name)

    @property
    def initialized(self) -> bool:
        """Return True if all services have been started."""
        return self._initialized