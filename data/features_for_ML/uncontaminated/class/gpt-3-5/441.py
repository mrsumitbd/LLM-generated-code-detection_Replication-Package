class AdaptiveKLController:
    """
    Adaptive KL controller described in the paper:
    https://arxiv.org/pdf/1909.08593.pdf
    """

    def __init__(self, init_kl_coef, target_kl, horizon):
        self.init_kl_coef = init_kl_coef
        self.target_kl = target_kl
        self.horizon = horizon
        self.kl_coef = init_kl_coef

    def update(self, current_kl, n_steps):
        if current_kl < self.target_kl / 1.5:
            self.kl_coef /= 2
        elif current_kl > self.target_kl * 1.5:
            self.kl_coef *= 2
        return self.kl_coef