import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from collections import deque
import os
import json

class Agent:

    def __init__(self, args):
        self.args = args
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._build_model()
        self.optimizer = optim.Adam(self.model.parameters(), lr=args.get('learning_rate', 1e-4))
        self.memory = deque(maxlen=args.get('memory_size', 10000))
        self.gamma = args.get('gamma', 0.99)
        self.epsilon = args.get('epsilon', 1.0)
        self.epsilon_decay = args.get('epsilon_decay', 0.995)
        self.epsilon_min = args.get('epsilon_min', 0.01)
        self.model_path = args.get('model_path', './model.pt')
        self.config_path = args.get('config_path', './config.json')

    def _build_model(self):
        model = nn.Sequential(
            nn.Linear(self.args.get('state_size', 512), 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, self.args.get('action_size', 64))
        )
        return model.to(self.device)

    def build_state(self, ob, info):
        state = {}
        state['observation'] = ob
        state['info'] = info
        return state

    def encode(self, observation, max_length=512):
        if isinstance(observation, str):
            tokens = observation.split()[:max_length]
            encoded = [hash(token) % 10000 for token in tokens]
            encoded += [0] * (max_length - len(encoded))
            return torch.tensor(encoded[:max_length], dtype=torch.float32, device=self.device)
        elif isinstance(observation, (list, tuple)):
            encoded = list(observation)[:max_length]
            encoded += [0] * (max_length - len(encoded))
            return torch.tensor(encoded[:max_length], dtype=torch.float32, device=self.device)
        else:
            return torch.zeros(max_length, dtype=torch.float32, device=self.device)

    def decode(self, act):
        if isinstance(act, torch.Tensor):
            return act.cpu().detach().numpy()
        elif isinstance(act, np.ndarray):
            return act
        else:
            return np.array(act)

    def encode_valids(self, valids, max_length=64):
        if isinstance(valids, (list, tuple)):
            encoded = list(valids)[:max_length]
            encoded += [0] * (max_length - len(encoded))
            return torch.tensor(encoded[:max_length], dtype=torch.float32, device=self.device)
        else:
            return torch.ones(max_length, dtype=torch.float32, device=self.device)

    def act(self, states, valid_acts, method='epsilon_greedy', state_strs=None, eps=0.1):
        if method == 'epsilon_greedy':
            if np.random.random() < eps:
                if isinstance(valid_acts, (list, tuple)) and len(valid_acts) > 0:
                    return np.random.choice(valid_acts)
                else:
                    return 0
            else:
                with torch.no_grad():
                    if isinstance(states, dict):
                        state_tensor = self.encode(str(states), max_length=512)
                    else:
                        state_tensor = self.encode(states, max_length=512)
                    state_tensor = state_tensor.unsqueeze(0)
                    q_values = self.model(state_tensor)
                    action = q_values.argmax(dim=1).item()
                    return action
        elif method == 'greedy':
            with torch.no_grad():
                if isinstance(states, dict):
                    state_tensor = self.encode(str(states), max_length=512)
                else:
                    state_tensor = self.encode(states, max_length=512)
                state_tensor = state_tensor.unsqueeze(0)
                q_values = self.model(state_tensor)
                action = q_values.argmax(dim=1).item()
                return action
        else:
            if isinstance(valid_acts, (list, tuple)) and len(valid_acts) > 0:
                return np.random.choice(valid_acts)
            else:
                return 0

    def update(self, transitions, last_values, step=None, rewards_invdy=None):
        if len(transitions) == 0:
            return
        
        batch_size = min(len(transitions), self.args.get('batch_size', 32))
        indices = np.random.choice(len(transitions), batch_size, replace=False)
        
        states = []
        actions = []
        rewards = []
        next_states = []
        dones = []
        
        for idx in indices:
            transition = transitions[idx]
            states.append(self.encode(str(transition[0]), max_length=512))
            actions.append(transition[1])
            rewards.append(transition[2])
            next_states.append(self.encode(str(transition[3]), max_length=512))
            dones.append(transition[4])
        
        states = torch.stack(states)
        actions = torch.tensor(actions, dtype=torch.long, device=self.device)
        rewards = torch.tensor(rewards, dtype=torch.float32, device=self.device)
        next_states = torch.stack(next_states)
        dones = torch.tensor(dones, dtype=torch.float32, device=self.device)
        
        q_values = self.model(states)
        q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
        
        with torch.no_grad():
            next_q_values = self.model(next_states).max(dim=1)[0]
            target_q_values = rewards + self.gamma * next_q_values * (1 - dones)
        
        loss = nn.MSELoss()(q_values, target_q_values)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def load(self):
        if os.path.exists(self.model_path):
            self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                self.epsilon = config.get('epsilon', self.epsilon)

    def save(self):
        torch.save(self.model.state_dict(), self.model_path)
        config = {'epsilon': self.epsilon}
        with open(self.config_path, 'w') as f:
            json.dump(config, f)