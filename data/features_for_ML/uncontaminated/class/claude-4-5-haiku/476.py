from typing import List, Dict, Any
import anthropic
import json
import re


class RecruiterAgent:
    """Recruitment agent: generates descriptions for work agents"""

    def __init__(self, agent_id: str, model_name: str = None, num_agents: int = 3):
        self.agent_id = agent_id
        self.model_name = model_name or "claude-3-5-sonnet-20241022"
        self.num_agents = num_agents
        self.client = anthropic.Anthropic()

    def _create_prompt(self, problem: str, feedback: str = None) -> str:
        base_prompt = f"""You are a recruitment agent tasked with creating descriptions for specialized work agents that will collaborate to solve problems.

Problem to solve:
{problem}

Your task is to generate descriptions for {self.num_agents} specialized agents that will work together to solve this problem. Each agent should have a specific role and expertise.

For each agent, provide:
1. Agent Name: A descriptive name for the agent
2. Role: The specific role this agent will play
3. Expertise: Key areas of expertise
4. Responsibilities: What this agent will be responsible for
5. Interaction Style: How this agent should interact with other agents

Format your response as a JSON array with {self.num_agents} objects, each containing the fields: "name", "role", "expertise", "responsibilities", and "interaction_style".

Ensure the agents have complementary skills and can work together effectively."""

        if feedback:
            base_prompt += f"\n\nPrevious feedback to improve upon:\n{feedback}"

        return base_prompt

    def _create_default_experts(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "Analyst",
                "role": "Problem Analysis and Decomposition",
                "expertise": ["Problem analysis", "Requirement gathering", "Task decomposition"],
                "responsibilities": ["Analyze the problem", "Break down into subtasks", "Identify constraints"],
                "interaction_style": "Provides structured analysis to guide other agents"
            },
            {
                "name": "Executor",
                "role": "Solution Implementation",
                "expertise": ["Implementation", "Execution", "Technical problem-solving"],
                "responsibilities": ["Execute solutions", "Handle technical details", "Implement strategies"],
                "interaction_style": "Receives guidance from Analyst, reports progress to Coordinator"
            },
            {
                "name": "Coordinator",
                "role": "Team Coordination and Integration",
                "expertise": ["Coordination", "Integration", "Quality assurance"],
                "responsibilities": ["Coordinate between agents", "Ensure quality", "Integrate results"],
                "interaction_style": "Facilitates communication and ensures coherent solution"
            }
        ]

    def recruit_agents(self, problem: str, feedback: str = None) -> List[Dict[str, Any]]:
        """Generate agent descriptions for the given problem"""
        prompt = self._create_prompt(problem, feedback)
        
        message = self.client.messages.create(
            model=self.model_name,
            max_tokens=2048,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            try:
                agents = json.loads(json_match.group())
                return agents
            except json.JSONDecodeError:
                return self._create_default_experts()
        
        return self._create_default_experts()

    def get_agent_descriptions(self, problem: str, feedback: str = None) -> str:
        """Get formatted descriptions of recruited agents"""
        agents = self.recruit_agents(problem, feedback)
        
        description = f"Recruited Agents for Problem: {problem}\n"
        description += "=" * 50 + "\n\n"
        
        for i, agent in enumerate(agents, 1):
            description += f"Agent {i}: {agent.get('name', 'Unknown')}\n"
            description += f"  Role: {agent.get('role', 'N/A')}\n"
            description += f"  Expertise: {', '.join(agent.get('expertise', []))}\n"
            description += f"  Responsibilities: {', '.join(agent.get('responsibilities', []))}\n"
            description += f"  Interaction Style: {agent.get('interaction_style', 'N/A')}\n\n"
        
        return description