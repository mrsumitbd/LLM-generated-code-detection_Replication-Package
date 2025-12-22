class AdaptiveKLController:
    """
    Adaptive KL controller described in the paper:
    https://arxiv.org/pdf/1909.08593.pdf
    """

    def __init__(self, init_kl_coef, target_kl, horizon):
        self.kl_coef = init_kl_coef
        self.target_kl = target_kl
        self.horizon = horizon

    def update(self, current_kl, n_steps):
        """
        Update the KL coefficient based on the current KL divergence.
        
        Args:
            current_kl: Current KL divergence value
            n_steps: Number of steps taken
        """
        if current_kl > self.target_kl * 1.5:
            self.kl_coef *= 1.5
        elif current_kl < self.target_kl / 1.5:
            self.kl_coef /= 1.5
        
        return self.kl_coef