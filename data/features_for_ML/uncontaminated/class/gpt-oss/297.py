from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Iterable, List, Optional, Tuple

# Assume OmniAgent is defined elsewhere with a signature like:
# class OmniAgent:
#     def run(self, task: Optional[Callable] = None, session_id: Optional[str] = None) -> Any:
#         ...

class ParallelAgent:
    """Runs a list of OmniAgents in parallel, each with its own optional task,
    sharing a session ID if provided."""

    def __init__(self, sub_agents: List["OmniAgent"], max_retries: int = 3):
        if not isinstance(sub_agents, Iterable):
            raise TypeError("sub_agents must be an iterable of OmniAgent instances")
        self.sub_agents: List["OmniAgent"] = list(sub_agents)
        if not isinstance(max_retries, int) or max_retries < 0:
            raise ValueError("max_retries must be a non‑negative integer")
        self.max_retries: int = max_retries

    def run(
        self,
        tasks: Optional[List[Optional[Callable]]] = None,
        session_id: Optional[str] = None,
    ) -> List[Any]:
        """
        Execute each sub‑agent in parallel.

        Parameters
        ----------
        tasks:
            A list of callables (or None) to pass to each agent. If None,
            all agents receive None. The list length must match the number
            of sub_agents.
        session_id:
            Optional session identifier to share among all agents.

        Returns
        -------
        List[Any]
            The results from each agent in the same order as sub_agents.
        """
        if tasks is None:
            tasks = [None] * len(self.sub_agents)
        if len(tasks) != len(self.sub_agents):
            raise ValueError("Length of tasks must match number of sub_agents")

        results: List[Any] = [None] * len(self.sub_agents)

        with ThreadPoolExecutor(max_workers=len(self.sub_agents)) as executor:
            futures = [
                executor.submit(
                    self._run_with_retry,
                    agent,
                    task,
                    session_id,
                    idx,
                )
                for idx, (agent, task) in enumerate(zip(self.sub_agents, tasks))
            ]

            for future in futures:
                idx, result = future.result()
                results[idx] = result

        return results

    def _run_with_retry(
        self,
        agent: "OmniAgent",
        task: Optional[Callable],
        session_id: Optional[str],
        idx: int,
    ) -> Tuple[int, Any]:
        attempts = 0
        while attempts <= self.max_retries:
            try:
                return idx, agent.run(task=task, session_id=session_id)
            except Exception as exc:
                attempts += 1
                if attempts > self.max_retries:
                    raise RuntimeError(
                        f"Agent at index {idx} failed after {self.max_retries} retries"
                    ) from exc
                # Exponential back‑off with a small base delay
                time.sleep(0.1 * (2 ** (attempts - 1)))

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"sub_agents={len(self.sub_agents)}, "
            f"max_retries={self.max_retries})"
        )