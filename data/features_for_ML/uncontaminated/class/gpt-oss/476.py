from typing import List, Dict, Any


class RecruiterAgent:
    """Recruitment agent: generates descriptions for work agents"""

    def __init__(self, agent_id: str, model_name: str = None, num_agents: int = 3):
        self.agent_id = agent_id
        self.model_name = model_name or "gpt-3.5-turbo"
        self.num_agents = num_agents
        self.default_experts = self._create_default_experts()

    def _create_prompt(self, problem: str, feedback: str = None) -> str:
        prompt = (
            f"You are a recruitment agent tasked with generating descriptions for "
            f"{self.num_agents} work agents to solve the following problem:\n\n"
            f"{problem}\n\n"
            f"Please provide a JSON array of agent descriptions, each containing "
            f"the fields 'role', 'skills', and 'description'."
        )
        if feedback:
            prompt += f"\n\nFeedback received: {feedback}"
        return prompt

    def _create_default_experts(self) -> List[Dict[str, Any]]:
        return [
            {
                "role": "Python Developer",
                "skills": ["Python", "Django", "REST APIs", "Unit Testing"],
                "description": "Expert in building scalable web applications using Python and Django."
            },
            {
                "role": "Data Scientist",
                "skills": ["Python", "Pandas", "Scikit-learn", "Data Visualization"],
                "description": "Specializes in data analysis, machine learning, and predictive modeling."
            },
            {
                "role": "DevOps Engineer",
                "skills": ["Docker", "Kubernetes", "CI/CD", "AWS"],
                "description": "Focuses on automating deployment pipelines and managing cloud infrastructure."
            }
        ]