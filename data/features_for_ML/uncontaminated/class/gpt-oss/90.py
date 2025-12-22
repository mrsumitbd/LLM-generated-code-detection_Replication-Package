import os
import pickle
import random
import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except ImportError:
    torch = None
    nn = None
    optim = None


class SimplePolicy(nn.Module):
    def __init__(self, input_dim, action_dim):
        super(SimplePolicy, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim)
        )

    def forward(self, x):
        return self.net(x)


class Agent:
    def __init__(self, args):
        """
        args: dict with keys:
            - input_dim: int, dimensionality of encoded observation
            - action_dim: int, number of possible actions
            - lr: float, learning rate
            - device: str, 'cpu' or 'cuda'
            - save_path: str, path to save model
        """
        self.input_dim = args.get("input_dim", 128)
        self.action_dim = args.get("action_dim", 10)
        self.lr = args.get("lr", 1e-3)
        self.device = torch.device(args.get("device", "cpu"))
        self.save_path = args.get("save_path", "./agent.pth")

        if torch is None:
            raise RuntimeError("PyTorch is required for this Agent implementation.")

        self.policy = SimplePolicy(self.input_dim, self.action_dim).to(self.device)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def build_state(self, ob, info):
        """
        Combine observation and info into a single state dictionary.
        """
        state = {"observation": ob, "info": info}
        return state

    def encode(self, observation, max_length=512):
        """
        Encode observation into a fixed-size tensor.
        """
        # Flatten observation and pad/truncate to max_length
        flat = np.array(observation).flatten()
        if len(flat) > max_length:
            flat = flat[:max_length]
        else:
            pad = np.zeros(max_length - len(flat), dtype=flat.dtype)
            flat = np.concatenate([flat, pad])
        tensor = torch.tensor(flat, dtype=torch.float32, device=self.device)
        return tensor

    def decode(self, act):
        """
        Convert action index to action representation.
        """
        # For simplicity, return the index itself
        return act

    def encode_valids(self, valids, max_length=64):
        """
        Encode valid actions as a binary mask tensor.
        """
        mask = np.zeros(max_length, dtype=np.float32)
        for v in valids:
            if 0 <= v < max_length:
                mask[v] = 1.0
        return torch.tensor(mask, device=self.device)

    def act(self, states, valid_acts, method, state_strs=None, eps=0.1):
        """
        Choose actions for a batch of states.
        - states: list of state dicts
        - valid_acts: list of lists of valid action indices
        - method: 'random', 'greedy', or 'epsilon'
        """
        actions = []
        for state, valids in zip(states, valid_acts):
            obs = state["observation"]
            encoded = self.encode(obs).unsqueeze(0)  # batch dim
            logits = self.policy(encoded).squeeze(0)  # shape: [action_dim]
            mask = self.encode_valids(valids, self.action_dim)
            masked_logits = logits * mask + (mask - 1) * 1e9  # large negative for invalid

            if method == "random":
                act = random.choice(valids) if valids else 0
            elif method == "greedy":
                act = int(torch.argmax(masked_logits).item())
            elif method == "epsilon":
                if random.random() < eps:
                    act = random.choice(valids) if valids else 0
                else:
                    act = int(torch.argmax(masked_logits).item())
            else:
                act = int(torch.argmax(masked_logits).item())

            actions.append(self.decode(act))
        return actions

    def update(self, transitions, last_values, step=None, rewards_invdy=None):
        """
        Perform a simple policy gradient update.
        transitions: list of (state, action, reward, next_state, done)
        last_values: list of value estimates for next states
        """
        # For simplicity, use REINFORCE with baseline
        if not transitions:
            return

        # Compute returns
        returns = []
        G = 0
        for _, _, reward, _, done in reversed(transitions):
            if done:
                G = 0
            G = reward + 0.99 * G
            returns.insert(0, G)

        # Convert to tensors
        obs_batch = torch.stack([self.encode(t[0]["observation"]) for t in transitions])
        actions_batch = torch.tensor([t[1] for t in transitions], dtype=torch.long, device=self.device)
        returns_batch = torch.tensor(returns, dtype=torch.float32, device=self.device)

        # Policy loss
        logits = self.policy(obs_batch)
        log_probs = nn.functional.log_softmax(logits, dim=1)
        selected_log_probs = log_probs[range(len(actions_batch)), actions_batch]
        loss = -torch.mean(selected_log_probs * returns_batch)

        # Backprop
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def load(self):
        """
        Load model parameters from file.
        """
        if os.path.exists(self.save_path):
            checkpoint = torch.load(self.save_path, map_location=self.device)
            self.policy.load_state_dict(checkpoint["policy_state_dict"])
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            print(f"Loaded agent from {self.save_path}")
        else:
            print(f"No checkpoint found at {self.save_path}")

    def save(self):
        """
        Save model parameters to file.
        """
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        torch.save(
            {
                "policy_state_dict": self.policy.state_dict(),
                "optimizer_state_dict": self.optimizer.state_dict(),
            },
            self.save_path,
        )
        print(f"Saved agent to {self.save_path}")