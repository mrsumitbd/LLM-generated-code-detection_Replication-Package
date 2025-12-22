class Service:
    """Represents a service that can be initialized and started."""

    def __init__(self, name: str):
        self.name = name
        self.is_initialized = False
        self.is_started = False

    def initialize(self) -> None:
        self.is_initialized = True

    def start(self) -> None:
        self.is_started = True

class AgentBootstrapper:
    """Handles all agent initialization in proper order.

    This class orchestrates the initialization of all services,
    ensuring dependencies are resolved and services start in
    the correct order.
    """

    def __init__(self):
        self._services = {}
        self._initialization_order = []
        self._initialized = False

    def _log_initialization_summary(self) -> None:
        for service in self._initialization_order:
            print(f"Service '{service.name}' initialized: {service.is_initialized}, started: {service.is_started}")

    def get_service(self, service_name: str) -> Service | None:
        return self._services.get(service_name, None)

    def add_service(self, service: Service) -> None:
        self._services[service.name] = service
        self._initialization_order.append(service)

    def initialize(self) -> None:
        for service in self._initialization_order:
            service.initialize()
        self._initialized = True

    def start(self) -> None:
        for service in self._initialization_order:
            service.start()

    @property
    def initialized(self) -> bool:
        return self._initialized