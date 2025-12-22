from __future__ import annotations
from typing import Optional, List, Dict, Callable
import os
import importlib.util
import sys
import logging

# Minimal placeholder classes for Agent and AgentConfig
class AgentConfig:
    def __init__(self, agent_name: str = "default_agent"):
        self.agent_name = agent_name

class Agent:
    def __init__(self, config: AgentConfig):
        self.name = config.agent_name
        self.history: List[Dict[str, str]] = []

    def send(self, message: str) -> str:
        # Dummy echo response
        response = f"Echo: {message}"
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": response})
        return response

# Main Shell class
class Shell:
    """Interactive CLI shell for dialog with Quantalogic agents."""

    def __init__(self, agent_config: Optional[AgentConfig] = None, cli_log_level: Optional[str] = None):
        self.agent_config = agent_config or AgentConfig()
        self.cli_log_level = cli_log_level or "INFO"
        logging.basicConfig(level=getattr(logging, self.cli_log_level.upper()))
        self._agent = Agent(self.agent_config)
        self._commands: Dict[str, Callable[[List[str]], None]] = {}
        self._register_builtin_commands()
        self._load_plugin_commands()

    @property
    def current_agent(self) -> Agent:
        return self._agent

    @property
    def current_message_history(self) -> List[Dict[str, str]]:
        return self._agent.history

    def _register_builtin_commands(self) -> None:
        def cmd_exit(args: List[str]) -> None:
            print("Exiting shell.")
            sys.exit(0)

        def cmd_help(args: List[str]) -> None:
            print("Available commands:")
            for name in sorted(self._commands):
                print(f"  {name}")

        def cmd_history(args: List[str]) -> None:
            for i, msg in enumerate(self._agent.history, 1):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                print(f"{i:3d} [{role}] {content}")

        def cmd_clear(args: List[str]) -> None:
            os.system('cls' if os.name == 'nt' else 'clear')

        self._commands.update({
            "exit": cmd_exit,
            "quit": cmd_exit,
            "help": cmd_help,
            "history": cmd_history,
            "clear": cmd_clear,
        })

    def _load_plugin_commands(self) -> None:
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        if not os.path.isdir(plugins_dir):
            return
        for filename in os.listdir(plugins_dir):
            if not filename.endswith(".py"):
                continue
            module_name = filename[:-3]
            file_path = os.path.join(plugins_dir, filename)
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                if hasattr(module, "register_commands"):
                    module.register_commands(self._commands)

    def bottom_toolbar(self) -> str:
        agent_name = self._agent.name
        msg_count = len(self._agent.history)
        return f"Agent: {agent_name} | Messages: {msg_count}"