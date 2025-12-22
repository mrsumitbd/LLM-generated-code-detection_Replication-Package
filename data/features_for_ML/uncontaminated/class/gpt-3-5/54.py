from typing import Optional, List, Dict

class Shell:
    """Interactive CLI shell for dialog with Quantalogic agents."""

    def __init__(self, agent_config: Optional[AgentConfig] = None, cli_log_level: Optional[str] = None):
        self.agent_config = agent_config
        self.cli_log_level = cli_log_level
        self.current_agent = None
        self.current_message_history = []

    @property
    def current_agent(self) -> Agent:
        return self.current_agent

    @property
    def current_message_history(self) -> List[Dict[str, str]]:
        return self.current_message_history

    def _register_builtin_commands(self) -> None:
        pass

    def _load_plugin_commands(self) -> None:
        pass

    def bottom_toolbar(self):
        pass