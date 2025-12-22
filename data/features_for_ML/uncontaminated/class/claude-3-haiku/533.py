class RolloutEnvState:
    """Per-environment variables for the rollout loop."""

    def __init__(self, env, policy, device, max_episode_steps, gamma, lam, use_gae, use_popart, use_value_clip, use_reward_scaling):
        self.env = env
        self.policy = policy
        self.device = device
        self.max_episode_steps = max_episode_steps
        self.gamma = gamma
        self.lam = lam
        self.use_gae = use_gae
        self.use_popart = use_popart
        self.use_value_clip = use_value_clip
        self.use_reward_scaling = use_reward_scaling

        self.obs = self.env.reset()
        self.done = False
        self.info = {}
        self.step = 0

        self.rewards = []
        self.values = []
        self.log_probs = []
        self.entropies = []
        self.actions = []
        self.states = []

    def step(self):
        action, value, log_prob, entropy, state = self.policy.act(self.obs, self.device)
        next_obs, reward, done, info = self.env.step(action)

        self.rewards.append(reward)
        self.values.append(value)
        self.log_probs.append(log_prob)
        self.entropies.append(entropy)
        self.actions.append(action)
        self.states.append(state)

        self.obs = next_obs
        self.done = done
        self.info = info
        self.step += 1

        return reward, done, info

    def reset(self):
        self.obs = self.env.reset()
        self.done = False
        self.info = {}
        self.step = 0

        self.rewards = []
        self.values = []
        self.log_probs = []
        self.entropies = []
        self.actions = []
        self.states = []