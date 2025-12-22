class RolloutEnvState:
    """Per-environment variables for the rollout loop."""
    
    def __init__(self, env, state):
        self.env = env
        self.state = state
        self.done = False
        self.total_reward = 0.0