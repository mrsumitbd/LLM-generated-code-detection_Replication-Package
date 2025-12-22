import random
from typing import List, Tuple, Dict, Any

class VectorizedGemEnv:
    """
    A simple vectorized environment that simulates a gem‑matching game.
    Each sub‑environment maintains an internal state (an integer 0‑9) and a
    step counter. The environment accepts a batch of actions and returns
    the next states, rewards, done flags and info dictionaries for each
    sub‑environment.
    """

    def __init__(self, num_envs: int = 1, max_steps: int = 5):
        """
        Parameters
        ----------
        num_envs : int, optional
            Number of parallel environments to run. Default is 1.
        max_steps : int, optional
            Number of steps after which an environment is considered done.
            Default is 5.
        """
        self.num_envs = num_envs
        self.max_steps = max_steps
        self.states: List[int] = [random.randint(0, 9) for _ in range(num_envs)]
        self.step_counts: List[int] = [0 for _ in range(num_envs)]
        self.dones: List[bool] = [False for _ in range(num_envs)]

    def reset(self) -> List[int]:
        """
        Reset all environments to a new random state.

        Returns
        -------
        List[int]
            The initial state of each environment.
        """
        self.states = [random.randint(0, 9) for _ in range(self.num_envs)]
        self.step_counts = [0 for _ in range(self.num_envs)]
        self.dones = [False for _ in range(self.num_envs)]
        return self.states.copy()

    def step(self, actions: List[int]) -> Tuple[List[int], List[float], List[bool], List[Dict[str, Any]]]:
        """
        Take a step in each environment using the provided actions.

        Parameters
        ----------
        actions : List[int]
            A list of actions, one per environment. Each action should be an
            integer in the range 0‑3.

        Returns
        -------
        Tuple[List[int], List[float], List[bool], List[Dict[str, Any]]]
            next_states, rewards, dones, infos
        """
        if len(actions) != self.num_envs:
            raise ValueError(f"Expected {self.num_envs} actions, got {len(actions)}")

        next_states = []
        rewards = []
        infos = []

        for i, action in enumerate(actions):
            if self.dones[i]:
                # If already done, keep state unchanged
                next_states.append(self.states[i])
                rewards.append(0.0)
                infos.append({"terminated": True})
                continue

            # Simple reward logic: reward 1.0 if action matches state, else 0.0
            reward = 1.0 if action == self.states[i] else 0.0
            rewards.append(reward)

            # Update state randomly
            self.states[i] = random.randint(0, 9)
            next_states.append(self.states[i])

            # Increment step counter and check for termination
            self.step_counts[i] += 1
            done = self.step_counts[i] >= self.max_steps
            self.dones[i] = done
            infos.append({"terminated": done})

        return next_states, rewards, self.dones.copy(), infos

    def render(self, mode: str = "human") -> None:
        """
        Render the current state of all environments.

        Parameters
        ----------
        mode : str, optional
            Rendering mode. Only 'human' is supported.
        """
        if mode != "human":
            raise NotImplementedError(f"Render mode {mode} not supported.")
        for i in range(self.num_envs):
            status = "DONE" if self.dones[i] else "RUNNING"
            print(f"Env {i}: State={self.states[i]}, Step={self.step_counts[i]}, Status={status}")

    def close(self) -> None:
        """
        Close the environment. No resources to release in this simple implementation.
        """
        pass