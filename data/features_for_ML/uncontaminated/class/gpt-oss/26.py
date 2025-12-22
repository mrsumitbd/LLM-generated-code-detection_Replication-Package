from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any


class Config:
    DEFAULT_MODEL = "gpt-4o"


@dataclass
class AgentState:
    last_action: str | None = None
    last_output: str | None = None
    continue_flag: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class SparkAnalysisAgent:
    """Optimized interactive LangGraph agent with enhanced terminal formatting."""

    def __init__(self, model: str = Config.DEFAULT_MODEL, verbose: bool = False):
        self.model = model
        self.verbose = verbose
        self.state: AgentState = AgentState()
        self.tools: List[Tuple[str, str]] = []
        self.graph: Dict[str, Any] = {}
        self._reset_state()
        self._create_graph()

    def _reset_state(self) -> None:
        """Reset the agent's internal state to defaults."""
        self.state = AgentState()
        if self.verbose:
            print("[SparkAnalysisAgent] State has been reset.")

    def _print_service_setup_instructions(self, services: Dict[str, bool]) -> None:
        """Print instructions for setting up services."""
        print("\n=== Service Setup Instructions ===")
        for name, enabled in services.items():
            status = "Enabled" if enabled else "Disabled"
            print(f"  • {name}: {status}")
        print("===================================\n")

    def _print_tools_table(self) -> None:
        """Print a formatted table of available tools."""
        if not self.tools:
            print("[SparkAnalysisAgent] No tools available.")
            return

        header = f"{'Tool Name':<20} | {'Description'}"
        separator = "-" * len(header)
        print("\n=== Available Tools ===")
        print(header)
        print(separator)
        for name, desc in self.tools:
            print(f"{name:<20} | {desc}")
        print("=======================\n")

    def _create_graph(self) -> None:
        """Create a simple graph structure for the agent."""
        self.graph = {
            "nodes": [],
            "edges": [],
            "metadata": {"model": self.model, "verbose": self.verbose},
        }
        if self.verbose:
            print("[SparkAnalysisAgent] Graph initialized.")

    def _get_system_prompt(self) -> str:
        """Return the system prompt used by the agent."""
        prompt = (
            f"System Prompt:\n"
            f"Model: {self.model}\n"
            f"Verbose: {self.verbose}\n"
            f"Please provide concise, actionable responses."
        )
        return prompt

    def _should_continue(self, state: AgentState) -> str:
        """Determine whether the agent should continue processing."""
        if state.continue_flag:
            return "continue"
        return "stop"