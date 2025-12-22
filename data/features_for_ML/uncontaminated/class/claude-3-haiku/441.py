class AdaptiveKLController:
    """
    Adaptive KL controller described in the paper:
    https://arxiv.org/pdf/1909.08593.pdf
    """

    def __init__(self, init_kl_coef, target_kl, horizon):
        self.kl_coef = init_kl_coef
        self.target_kl = target_kl
        self.horizon = horizon
        self.step_count = 0

    def update(self, current_kl, n_steps):
        self.step_count += n_steps
        if current_kl > self.target_kl:
            self.kl_coef *= (1 + (self.step_count / self.horizon))
        else:
            self.kl_coef *= (1 - (self.step_count / self.horizon))
        self.kl_coef = max(self.kl_coef, 0.0)