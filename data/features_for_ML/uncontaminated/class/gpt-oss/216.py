import os
import gym
import numpy as np
import ray
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

@ray.remote
class TaskRunner:
    """Ray remote class for executing distributed PPO training tasks.

    This class encapsulates the main training logic and runs as a Ray remote actor
    to enable distributed execution across multiple nodes and GPUs.
    """

    def run(self, config):
        """
        Execute a PPO training task based on the provided configuration.

        Parameters
        ----------
        config : dict
            Configuration dictionary containing training parameters.
            Expected keys:
                - env_id (str): Gym environment ID.
                - total_timesteps (int): Total number of training timesteps.
                - learning_rate (float or callable): Learning rate.
                - n_steps (int): Number of steps to run per environment per update.
                - batch_size (int): Batch size for training.
                - gamma (float): Discount factor.
                - n_epochs (int): Number of epochs per update.
                - seed (int, optional): Random seed.
                - device (str, optional): 'cpu' or 'cuda'.
                - verbose (int, optional): Verbosity level.
                - output_dir (str, optional): Directory to save the trained model.
                - eval_episodes (int, optional): Number of episodes for evaluation.
                - eval_kwargs (dict, optional): Additional kwargs for evaluate_policy.

        Returns
        -------
        dict
            Dictionary containing training results:
                - mean_reward (float): Mean reward over evaluation episodes.
                - std_reward (float): Standard deviation of reward over evaluation episodes.
                - model_path (str): Path to the saved model.
        """
        # Extract configuration with defaults
        env_id = config.get("env_id", "CartPole-v1")
        total_timesteps = config.get("total_timesteps", 100_000)
        learning_rate = config.get("learning_rate", 3e-4)
        n_steps = config.get("n_steps", 2048)
        batch_size = config.get("batch_size", 64)
        gamma = config.get("gamma", 0.99)
        n_epochs = config.get("n_epochs", 10)
        seed = config.get("seed", None)
        device = config.get("device", "cpu")
        verbose = config.get("verbose", 0)
        output_dir = config.get("output_dir", "./ppo_models")
        eval_episodes = config.get("eval_episodes", 10)
        eval_kwargs = config.get("eval_kwargs", {})

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)
            gym.utils.seeding.seed(seed)

        # Create vectorized environment
        def make_env():
            env = gym.make(env_id)
            if seed is not None:
                env.seed(seed)
            return env

        vec_env = DummyVecEnv([make_env])

        # Initialize PPO model
        model = PPO(
            "MlpPolicy",
            vec_env,
            learning_rate=learning_rate,
            n_steps=n_steps,
            batch_size=batch_size,
            gamma=gamma,
            n_epochs=n_epochs,
            seed=seed,
            device=device,
            verbose=verbose,
        )

        # Train the model
        model.learn(total_timesteps=total_timesteps)

        # Save the trained model
        model_path = os.path.join(output_dir, f"ppo_{env_id.replace('-', '_')}.zip")
        model.save(model_path)

        # Evaluate the trained policy
        mean_reward, std_reward = evaluate_policy(
            model,
            vec_env,
            n_eval_episodes=eval_episodes,
            return_episode_rewards=False,
            **eval_kwargs,
        )

        return {
            "mean_reward": mean_reward,
            "std_reward": std_reward,
            "model_path": model_path,
        }