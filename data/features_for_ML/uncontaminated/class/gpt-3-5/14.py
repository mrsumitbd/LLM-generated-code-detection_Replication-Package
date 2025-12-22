class AsyncAgentsResourceWithRawResponse:

    def __init__(self, agents: AsyncAgentsResource) -> None:
        self.agents = agents

    async def get_agent(self, agent_id: str) -> dict:
        return await self.agents.get_agent(agent_id)

    async def create_agent(self, agent_data: dict) -> dict:
        return await self.agents.create_agent(agent_data)

    async def update_agent(self, agent_id: str, agent_data: dict) -> dict:
        return await self.agents.update_agent(agent_id, agent_data)

    async def delete_agent(self, agent_id: str) -> dict:
        return await self.agents.delete_agent(agent_id)