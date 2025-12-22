from typing import List, Dict, Any

class RecruiterAgent:
    """Recruitment agent: generates descriptions for work agents"""

    def __init__(self, agent_id: str, model_name: str = None, num_agents: int = 3):
        self.agent_id = agent_id
        self.model_name = model_name or "default_model"
        self.num_agents = num_agents
        self.experts = self._create_default_experts()

    def _create_prompt(self, problem: str, feedback: str = None) -> str:
        prompt = f"Generate {self.num_agents} unique job descriptions for the following problem: {problem}"
        if feedback:
            prompt += f"\nFeedback: {feedback}"
        return prompt

    def _create_default_experts(self) -> List[Dict[str, Any]]:
        return [
            {"name": "Expert 1", "expertise": ["software engineering", "project management"]},
            {"name": "Expert 2", "expertise": ["data analysis", "machine learning"]},
            {"name": "Expert 3", "expertise": ["content creation", "marketing"]}
        ]