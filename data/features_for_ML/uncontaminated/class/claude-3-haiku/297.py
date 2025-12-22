from typing import List

class ParallelAgent:
    """Runs a list of OmniAgents in parallel, each with its own optional task, sharing a session ID if provided."""

    def __init__(self, sub_agents: List[OmniAgent], max_retries: int = 3):
        self.sub_agents = sub_agents
        self.max_retries = max_retries
        self.session_id = None

    def set_session_id(self, session_id: str):
        self.session_id = session_id

    def run(self):
        results = []
        for agent in self.sub_agents:
            if self.session_id:
                agent.set_session_id(self.session_id)
            retries = 0
            while retries < self.max_retries:
                try:
                    result = agent.run()
                    results.append(result)
                    break
                except Exception as e:
                    retries += 1
                    if retries >= self.max_retries:
                        raise e
        return results