from typing import Any


class AgentClient:
    """
    Client class for Agent service.
    """

    def __init__(self, config: Any):
        self.config = config
        self._initialize_agent_model(config)

    def _initialize_agent_model(self, config: Any):
        """
        Instantiate the underlying agent model based on the provided configuration.
        """
        try:
            # Attempt to import the real Agent implementation
            from .agent import Agent  # type: ignore
        except Exception:
            # Fallback: minimal placeholder implementation
            class Agent:
                def __init__(self, cfg: Any):
                    self.cfg = cfg

                def __repr__(self):
                    return f"<Agent cfg={self.cfg!r}>"

            # Use the placeholder
        self._agent_model = Agent(config)

    def __getattr__(self, attr_name: str):
        """
        Delegate attribute access to the underlying agent model.
        """
        if hasattr(self._agent_model, attr_name):
            return getattr(self._agent_model, attr_name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{attr_name}'"
        )