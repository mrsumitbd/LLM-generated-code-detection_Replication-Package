class AgentClient:
    """
    Client class for Agent service.
    """

    def __init__(self, config: AgentCfg):
        self.config = config
        self._agent_model = None
        self._initialize_agent_model(config)

    def _initialize_agent_model(self, config: AgentCfg):
        """Initialize the agent model based on configuration."""
        try:
            if config.model_type == "local":
                from .local_agent import LocalAgent
                self._agent_model = LocalAgent(config)
            elif config.model_type == "remote":
                from .remote_agent import RemoteAgent
                self._agent_model = RemoteAgent(config)
            else:
                raise ValueError(f"Unknown model type: {config.model_type}")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize agent model: {str(e)}")

    def __getattr__(self, attr_name: str):
        """Delegate attribute access to the underlying agent model."""
        if attr_name in ('config', '_agent_model', '_initialize_agent_model'):
            return object.__getattribute__(self, attr_name)
        
        if self._agent_model is None:
            raise RuntimeError("Agent model not initialized")
        
        agent_attr = getattr(self._agent_model, attr_name)
        return agent_attr