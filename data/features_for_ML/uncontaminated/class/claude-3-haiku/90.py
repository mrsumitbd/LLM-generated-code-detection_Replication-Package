import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import deque

class Agent:
    def __init__(self, args):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.build_model(args)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=args.lr)
        self.gamma = args.gamma
        self.buffer = deque(maxlen=args.buffer_size)

    def build_model(self, args):
        model = nn.Sequential(
            nn.Linear(args.state_size, args.hidden_size),
            nn.ReLU(),
            nn.Linear(args.hidden_size, args.action_size)
        )
        return model.to(self.device)

    def build_state(self, ob, info):
        state = torch.tensor(ob, dtype=torch.float32, device=self.device)
        return state

    def encode(self, observation, max_length=512):
        return torch.tensor(observation, dtype=torch.long, device=self.device)

    def decode(self, act):
        return act.item()

    def encode_valids(self, valids, max_length=64):
        return torch.tensor(valids, dtype=torch.long, device=self.device)

    def act(self, states, valid_acts, method, state_strs=None, eps=0.1):
        if method == "random":
            return torch.randint(0, len(valid_acts), (1,), device=self.device)
        elif method == "greedy":
            with torch.no_grad():
                logits = self.model(states)
                logits[~valid_acts] = -float("inf")
                return logits.argmax(dim=-1)
        elif method == "epsilon-greedy":
            with torch.no_grad():
                logits = self.model(states)
                logits[~valid_acts] = -float("inf")
                if np.random.rand() < eps:
                    return torch.randint(0, len(valid_acts), (1,), device=self.device)
                else:
                    return logits.argmax(dim=-1)

    def update(self, transitions, last_values, step=None, rewards_invdy=None):
        states, actions, rewards, next_states, dones = zip(*transitions)
        states = torch.stack(states)
        actions = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        next_states = torch.stack(next_states)
        dones = torch.tensor(dones, dtype=torch.float32, device=self.device)

        with torch.no_grad():
            next_values = self.model(next_states).max(dim=-1)[0]
            targets = rewards + self.gamma * (1 - dones) * next_values

        loss = F.mse_loss(self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1), targets)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def load(self):
        pass

    def save(self):
        pass