import os
import gym
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Normal
from collections import deque

def run_ppo(config, compute_score=None):
    env = gym.make(config.env_name)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.shape[0]

    class Actor(nn.Module):
        def __init__(self, state_dim, action_dim):
            super().__init__()
            self.fc1 = nn.Linear(state_dim, 64)
            self.fc2 = nn.Linear(64, 64)
            self.mu = nn.Linear(64, action_dim)
            self.sigma = nn.Linear(64, action_dim)

        def forward(self, state):
            x = torch.relu(self.fc1(state))
            x = torch.relu(self.fc2(x))
            mu = torch.tanh(self.mu(x))
            sigma = torch.exp(self.sigma(x))
            return mu, sigma

    class Critic(nn.Module):
        def __init__(self, state_dim):
            super().__init__()
            self.fc1 = nn.Linear(state_dim, 64)
            self.fc2 = nn.Linear(64, 64)
            self.value = nn.Linear(64, 1)

        def forward(self, state):
            x = torch.relu(self.fc1(state))
            x = torch.relu(self.fc2(x))
            value = self.value(x)
            return value

    actor = Actor(state_dim, action_dim).to(config.device)
    critic = Critic(state_dim).to(config.device)
    actor_optimizer = optim.Adam(actor.parameters(), lr=config.actor_lr)
    critic_optimizer = optim.Adam(critic.parameters(), lr=config.critic_lr)

    episode_rewards = deque(maxlen=100)
    for episode in range(config.num_episodes):
        state = env.reset()
        done = False
        episode_reward = 0

        while not done:
            action_mean, action_std = actor(torch.tensor(state, dtype=torch.float32, device=config.device))
            action = torch.normal(action_mean, action_std).cpu().detach().numpy()
            next_state, reward, done, _ = env.step(action)
            episode_reward += reward

            if compute_score is not None:
                compute_score(episode, state, action, reward, next_state, done)

            state = next_state

        episode_rewards.append(episode_reward)
        print(f"Episode {episode}, Reward: {episode_reward:.2f}")

    return actor, critic