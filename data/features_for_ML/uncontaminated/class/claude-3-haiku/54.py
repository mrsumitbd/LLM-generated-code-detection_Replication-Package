from typing import Optional, List, Dict
from agent import Agent, AgentConfig

class Shell:
    """Interactive CLI shell for dialog with Quantalogic agents."""

    def __init__(self, agent_config: Optional[AgentConfig] = None, cli_log_level: Optional[str] = None):
        self._agent_config = agent_config
        self._cli_log_level = cli_log_level
        self._agent = None
        self._message_history = []
        self._register_builtin_commands()
        self._load_plugin_commands()

    @property
    def current_agent(self) -> Agent:
        if self._agent is None:
            self._agent = Agent(self._agent_config)
        return self._agent

    @property
    def current_message_history(self) -> List[Dict[str, str]]:
        return self._message_history

    def _register_builtin_commands(self) -> None:
        # Register built-in commands
        pass

    def _load_plugin_commands(self) -> None:
        # Load and register plugin commands
        pass

    def bottom_toolbar(self):
        # Implement the bottom toolbar
        pass