class AsyncAgentsResourceWithRawResponse:
    def __init__(self, agents: AsyncAgentsResource) -> None:
        self.agents = agents

    async def get_agents(self, **kwargs) -> Tuple[dict, requests.Response]:
        response = await self.agents.get_agents(**kwargs)
        return response.json(), response

    async def get_agent(self, agent_id: str, **kwargs) -> Tuple[dict, requests.Response]:
        response = await self.agents.get_agent(agent_id, **kwargs)
        return response.json(), response

    async def create_agent(self, data: dict, **kwargs) -> Tuple[dict, requests.Response]:
        response = await self.agents.create_agent(data, **kwargs)
        return response.json(), response

    async def update_agent(self, agent_id: str, data: dict, **kwargs) -> Tuple[dict, requests.Response]:
        response = await self.agents.update_agent(agent_id, data, **kwargs)
        return response.json(), response

    async def delete_agent(self, agent_id: str, **kwargs) -> Tuple[dict, requests.Response]:
        response = await self.agents.delete_agent(agent_id, **kwargs)
        return response.json(), response