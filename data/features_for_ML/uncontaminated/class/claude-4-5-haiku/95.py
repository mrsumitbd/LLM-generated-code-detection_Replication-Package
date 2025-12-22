import numpy as np
import anthropic


class VectorizedGemEnv:
    """A vectorized environment for interacting with Claude through the Anthropic API."""

    def __init__(self):
        """Initialize the VectorizedGemEnv with Anthropic client and configuration."""
        self.client = anthropic.Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.conversations = {}
        self.next_env_id = 0

    def reset(self, num_envs: int = 1) -> tuple[np.ndarray, np.ndarray]:
        """Reset the environment and create new conversation threads.
        
        Args:
            num_envs: Number of parallel environments to create
            
        Returns:
            Tuple of (env_ids, initial_observations)
        """
        env_ids = np.arange(self.next_env_id, self.next_env_id + num_envs)
        self.next_env_id += num_envs

        for env_id in env_ids:
            self.conversations[env_id] = []

        initial_obs = np.array([f"Environment {env_id} initialized" for env_id in env_ids])
        return env_ids, initial_obs

    def step(self, env_ids: np.ndarray, actions: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Execute actions in the environments and get responses from Claude.
        
        Args:
            env_ids: Array of environment IDs
            actions: Array of prompts/actions to send to Claude
            
        Returns:
            Tuple of (observations, rewards, dones)
        """
        observations = []
        rewards = []
        dones = []

        for env_id, action in zip(env_ids, actions):
            if env_id not in self.conversations:
                self.conversations[env_id] = []

            self.conversations[env_id].append({"role": "user", "content": action})

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=self.conversations[env_id],
            )

            assistant_message = response.content[0].text
            self.conversations[env_id].append({"role": "assistant", "content": assistant_message})

            observations.append(assistant_message)
            rewards.append(1.0)
            dones.append(False)

        return np.array(observations), np.array(rewards), np.array(dones)

    def close(self):
        """Close the environment and clean up resources."""
        self.conversations.clear()
        self.next_env_id = 0


def main():
    """Main function to demonstrate VectorizedGemEnv usage."""
    env = VectorizedGemEnv()

    env_ids, obs = env.reset(num_envs=2)
    print("Initial observations:")
    for env_id, ob in zip(env_ids, obs):
        print(f"  Env {env_id}: {ob}")

    actions = np.array(["What is 2+2?", "Tell me a short joke"])
    obs, rewards, dones = env.step(env_ids, actions)

    print("\nResponses from Claude:")
    for env_id, ob, reward in zip(env_ids, obs, rewards):
        print(f"  Env {env_id} (reward={reward}): {ob[:100]}...")

    actions = np.array(["What about 3+3?", "Tell me another joke"])
    obs, rewards, dones = env.step(env_ids, actions)

    print("\nSecond round responses:")
    for env_id, ob, reward in zip(env_ids, obs, rewards):
        print(f"  Env {env_id} (reward={reward}): {ob[:100]}...")

    env.close()


if __name__ == "__main__":
    main()