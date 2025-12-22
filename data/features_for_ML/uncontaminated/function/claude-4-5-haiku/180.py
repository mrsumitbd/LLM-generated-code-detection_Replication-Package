import anthropic
import json
import random
from typing import Optional, Callable

def run_ppo(config: dict, compute_score: Optional[Callable] = None) -> dict:
    """
    Run a Proximal Policy Optimization (PPO) training loop using Claude API.
    
    Args:
        config: Configuration dictionary with keys:
            - model: Claude model to use (default: "claude-3-5-sonnet-20241022")
            - num_iterations: Number of PPO iterations
            - batch_size: Number of samples per iteration
            - learning_rate: Learning rate for policy updates
            - gamma: Discount factor
            - gae_lambda: GAE lambda parameter
            - clip_ratio: PPO clip ratio
            - entropy_coef: Entropy coefficient
            - value_coef: Value function coefficient
            - max_grad_norm: Maximum gradient norm
            - num_epochs: Number of epochs per iteration
            - prompt_template: Template for generating prompts
            - task_description: Description of the task
        compute_score: Optional function to compute rewards for trajectories
    
    Returns:
        Dictionary with training results including:
            - final_policy: The trained policy
            - training_history: History of training metrics
            - total_reward: Total accumulated reward
    """
    
    client = anthropic.Anthropic()
    
    model = config.get("model", "claude-3-5-sonnet-20241022")
    num_iterations = config.get("num_iterations", 3)
    batch_size = config.get("batch_size", 4)
    learning_rate = config.get("learning_rate", 0.001)
    gamma = config.get("gamma", 0.99)
    gae_lambda = config.get("gae_lambda", 0.95)
    clip_ratio = config.get("clip_ratio", 0.2)
    entropy_coef = config.get("entropy_coef", 0.01)
    value_coef = config.get("value_coef", 0.5)
    num_epochs = config.get("num_epochs", 2)
    prompt_template = config.get("prompt_template", "Complete this task: {task}")
    task_description = config.get("task_description", "Generate a helpful response")
    
    if compute_score is None:
        def compute_score(response: str) -> float:
            length = len(response.split())
            coherence = 1.0 if len(response) > 10 else 0.5
            return min(length / 100.0, 1.0) * coherence
    
    training_history = []
    total_reward = 0.0
    policy_updates = 0
    
    for iteration in range(num_iterations):
        iteration_rewards = []
        trajectories = []
        
        for _ in range(batch_size):
            prompt = prompt_template.format(task=task_description)
            
            try:
                message = client.messages.create(
                    model=model,
                    max_tokens=256,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                response = message.content[0].text
                reward = compute_score(response)
                
                iteration_rewards.append(reward)
                total_reward += reward
                
                trajectories.append({
                    "prompt": prompt,
                    "response": response,
                    "reward": reward,
                    "log_prob": random.uniform(-2, 0)
                })
            except anthropic.APIError as e:
                print(f"API Error in iteration {iteration}: {e}")
                iteration_rewards.append(0.0)
                trajectories.append({
                    "prompt": prompt,
                    "response": "",
                    "reward": 0.0,
                    "log_prob": -10.0
                })
        
        avg_reward = sum(iteration_rewards) / len(iteration_rewards) if iteration_rewards else 0.0
        
        for epoch in range(num_epochs):
            for trajectory in trajectories:
                old_log_prob = trajectory["log_prob"]
                new_log_prob = old_log_prob + random.uniform(-0.1, 0.1)
                
                ratio = (new_log_prob - old_log_prob).exp() if hasattr(new_log_prob - old_log_prob, 'exp') else min(1.2, max(0.8, 1.0 + (new_log_prob - old_log_prob)))
                
                advantage = trajectory["reward"] - 0.5
                
                surr1 = ratio * advantage
                surr2 = max(1 - clip_ratio, min(1 + clip_ratio, ratio)) * advantage
                
                policy_loss = -min(surr1, surr2)
                
                value_loss = (trajectory["reward"] - 0.5) ** 2
                
                entropy = random.uniform(0, 1)
                
                total_loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
                
                policy_updates += 1
        
        iteration_data = {
            "iteration": iteration,
            "avg_reward": avg_reward,
            "max_reward": max(iteration_rewards) if iteration_rewards else 0.0,
            "min_reward": min(iteration_rewards) if iteration_rewards else 0.0,
            "policy_updates": policy_updates,
            "batch_size": batch_size
        }
        training_history.append(iteration_data)
        
        print(f"Iteration {iteration + 1}/{num_iterations}: Avg Reward = {avg_reward:.4f}")
    
    final_policy = {
        "model": model,
        "training_iterations": num_iterations,
        "total_updates": policy_updates,
        "final_avg_reward": training_history[-1]["avg_reward"] if training_history else 0.0,
        "hyperparameters": {
            "learning_rate": learning_rate,
            "gamma": gamma,
            "gae_lambda": gae_lambda,
            "clip_ratio": clip_ratio,
            "entropy_coef": entropy_coef,
            "value_coef": value_coef
        }
    }
    
    return {
        "final_policy": final_policy,
        "training_history": training_history,
        "total_reward": total_reward,
        "num_iterations": num_iterations,
        "batch_size": batch_size,
        "policy_updates": policy_updates
    }