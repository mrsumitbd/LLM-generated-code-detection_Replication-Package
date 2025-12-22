import requests
from dataclasses import dataclass

@dataclass
class AgentCard:
    agent_id: str
    agent_name: str
    agent_url: str
    agent_description: str
    agent_image: str

class A2ACardResolver:
    def __init__(self, base_url, agent_card_path="/.well-known/agent.json"):
        self.base_url = base_url
        self.agent_card_path = agent_card_path

    def get_agent_card(self) -> AgentCard:
        url = f"{self.base_url}{self.agent_card_path}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return AgentCard(
            agent_id=data["agent_id"],
            agent_name=data["agent_name"],
            agent_url=data["agent_url"],
            agent_description=data["agent_description"],
            agent_image=data["agent_image"]
        )