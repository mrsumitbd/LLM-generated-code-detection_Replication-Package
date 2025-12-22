from typing import List, Dict, Any

class RecruiterAgent:
    """Recruitment agent: generates descriptions for work agents"""

    def __init__(self, agent_id: str, model_name: str = None, num_agents: int = 3):
        self.agent_id = agent_id
        self.model_name = model_name
        self.num_agents = num_agents

    def _create_prompt(self, problem: str, feedback: str = None) -> str:
        if feedback:
            return f"Agent {self.agent_id} is tasked with solving the problem: {problem}. Feedback: {feedback}"
        else:
            return f"Agent {self.agent_id} is tasked with solving the problem: {problem}"

    def _create_default_experts(self) -> List[Dict[str, Any]]:
        default_experts = []
        for i in range(self.num_agents):
            expert = {
                "agent_id": f"Expert_{i+1}",
                "model_name": self.model_name if self.model_name else "Default Model"
            }
            default_experts.append(expert)
        return default_experts