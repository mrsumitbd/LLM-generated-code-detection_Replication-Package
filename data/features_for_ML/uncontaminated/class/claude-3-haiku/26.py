import os
from typing import Dict
from langchain.agents import AgentState
from config import Config

class SparkAnalysisAgent:
    """Optimized interactive LangGraph agent with enhanced terminal formatting."""

    def __init__(self, model: str = Config.DEFAULT_MODEL, verbose: bool = False):
        self.model = model
        self.verbose = verbose
        self._reset_state()

    def _reset_state(self) -> None:
        self.state = AgentState()
        self.state.tools = []
        self.state.services = {
            "spark": False,
            "hdfs": False,
            "hive": False,
            "kafka": False,
        }

    def _print_service_setup_instructions(self, services: Dict[str, bool]) -> None:
        for service, is_setup in services.items():
            if not is_setup:
                print(f"Please set up {service} service before continuing.")

    def _print_tools_table(self) -> None:
        print("Available tools:")
        for tool in self.state.tools:
            print(f"- {tool.name}")

    def _create_graph(self) -> None:
        self.state.graph = LangGraph()

    def _get_system_prompt(self) -> str:
        return "I'm an AI assistant here to help you with Spark analysis. How can I assist you today?"

    def _should_continue(self, state: AgentState) -> str:
        if not state.services["spark"]:
            return "Please set up the Spark service before continuing."
        if not state.tools:
            return "No tools available. Please add tools to the agent."
        return None