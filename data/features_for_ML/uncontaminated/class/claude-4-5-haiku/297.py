class ParallelAgent:
    """Runs a list of OmniAgents in parallel, each with its own optional task, sharing a session ID if provided."""

    def __init__(self, sub_agents: List[OmniAgent], max_retries: int = 3):
        self.sub_agents = sub_agents
        self.max_retries = max_retries
        self.session_id = None

    def set_session_id(self, session_id: str) -> None:
        """Set the session ID for all sub-agents."""
        self.session_id = session_id
        for agent in self.sub_agents:
            agent.set_session_id(session_id)

    async def run_parallel(self, tasks: List[str] = None) -> List[Any]:
        """
        Run all sub-agents in parallel with optional tasks.
        
        Args:
            tasks: Optional list of tasks, one per agent. If None, agents run without tasks.
        
        Returns:
            List of results from each agent.
        """
        import asyncio
        
        if tasks is None:
            tasks = [None] * len(self.sub_agents)
        
        if len(tasks) != len(self.sub_agents):
            raise ValueError("Number of tasks must match number of sub-agents")
        
        coroutines = []
        for agent, task in zip(self.sub_agents, tasks):
            if task is None:
                coroutines.append(agent.run())
            else:
                coroutines.append(agent.run(task))
        
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        return results

    def run_parallel_sync(self, tasks: List[str] = None) -> List[Any]:
        """
        Synchronous wrapper for running agents in parallel.
        
        Args:
            tasks: Optional list of tasks, one per agent. If None, agents run without tasks.
        
        Returns:
            List of results from each agent.
        """
        import asyncio
        
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.run_parallel(tasks))

    def get_sub_agent(self, index: int) -> OmniAgent:
        """Get a specific sub-agent by index."""
        return self.sub_agents[index]

    def add_sub_agent(self, agent: OmniAgent) -> None:
        """Add a new sub-agent to the parallel agent."""
        self.sub_agents.append(agent)
        if self.session_id:
            agent.set_session_id(self.session_id)

    def remove_sub_agent(self, index: int) -> None:
        """Remove a sub-agent by index."""
        if 0 <= index < len(self.sub_agents):
            self.sub_agents.pop(index)

    def get_sub_agents_count(self) -> int:
        """Get the number of sub-agents."""
        return len(self.sub_agents)