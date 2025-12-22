from typing import List

class ParallelAgent:
    """Runs a list of OmniAgents in parallel, each with its own optional task, sharing a session ID if provided."""

    def __init__(self, sub_agents: List[OmniAgent], max_retries: int = 3):
        self.sub_agents = sub_agents
        self.max_retries = max_retries

    def run_agents(self):
        for agent in self.sub_agents:
            agent.run(self.max_retries)

class OmniAgent:
    def __init__(self, task=None, session_id=None):
        self.task = task
        self.session_id = session_id

    def run(self, max_retries):
        print(f"Running agent with task: {self.task}, session ID: {self.session_id}, max retries: {max_retries}")

# Usage example
sub_agents = [OmniAgent(task="Task 1", session_id="123"), OmniAgent(task="Task 2")]
parallel_agent = ParallelAgent(sub_agents)
parallel_agent.run_agents()