def run_ppo(config, compute_score=None):
    if compute_score is None:
        def compute_score(state):
            return 0
    # Add your PPO algorithm implementation here
    pass