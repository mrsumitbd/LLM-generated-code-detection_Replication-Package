class A2ACardResolver:

    def __init__(self, base_url, agent_card_path="/.well-known/agent.json"):
        self.base_url = base_url
        self.agent_card_path = agent_card_path

    def get_agent_card(self) -> AgentCard:
        import requests
        import json
        
        url = self.base_url.rstrip('/') + self.agent_card_path
        response = requests.get(url)
        response.raise_for_status()
        
        agent_card_data = response.json()
        return AgentCard(**agent_card_data)