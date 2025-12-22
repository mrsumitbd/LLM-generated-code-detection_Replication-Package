class AgentBootstrapper:
    """Handles all agent initialization in proper order.

    This class orchestrates the initialization of all services,
    ensuring dependencies are resolved and services start in
    the correct order.
    """

    def __init__(self):
        self._services: dict[str, Service] = {}
        self._initialization_order: list[str] = []
        self._initialized: bool = False

    def _log_initialization_summary(self) -> None:
        """Log a summary of initialized services."""
        if not self._initialized:
            return
        
        summary_lines = [
            "Agent Initialization Summary:",
            f"Total Services Initialized: {len(self._services)}",
            "Initialization Order:"
        ]
        
        for idx, service_name in enumerate(self._initialization_order, 1):
            summary_lines.append(f"  {idx}. {service_name}")
        
        summary = "\n".join(summary_lines)
        print(summary)

    def get_service(self, service_name: str) -> 'Service | None':
        """Retrieve a service by name.
        
        Args:
            service_name: The name of the service to retrieve.
            
        Returns:
            The service instance if found, None otherwise.
        """
        return self._services.get(service_name)

    def register_service(self, service_name: str, service: 'Service', dependencies: list[str] | None = None) -> None:
        """Register a service with optional dependencies.
        
        Args:
            service_name: The name of the service.
            service: The service instance.
            dependencies: List of service names this service depends on.
        """
        if dependencies is None:
            dependencies = []
        
        # Verify all dependencies are already registered
        for dep in dependencies:
            if dep not in self._services:
                raise ValueError(f"Dependency '{dep}' not found for service '{service_name}'")
        
        self._services[service_name] = service
        self._initialization_order.append(service_name)

    def initialize(self) -> None:
        """Initialize all registered services in order."""
        for service_name in self._initialization_order:
            service = self._services[service_name]
            if hasattr(service, 'initialize'):
                service.initialize()
        
        self._initialized = True
        self._log_initialization_summary()

    @property
    def initialized(self) -> bool:
        """Check if all services have been initialized.
        
        Returns:
            True if initialization is complete, False otherwise.
        """
        return self._initialized