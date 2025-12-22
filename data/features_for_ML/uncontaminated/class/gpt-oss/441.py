import math

class AdaptiveKLController:
    """
    Adaptive KL controller described in the paper:
    https://arxiv.org/pdf/1909.08593.pdf
    """

    def __init__(self, init_kl_coef, target_kl, horizon):
        """
        Parameters
        ----------
        init_kl_coef : float
            Initial KL coefficient.
        target_kl : float
            Desired KL divergence.
        horizon : int
            Number of steps between updates (used for optional throttling).
        """
        self.kl_coef = float(init_kl_coef)
        self.target_kl = float(target_kl)
        self.horizon = int(horizon)
        self._steps_since_update = 0

    def update(self, current_kl, n_steps):
        """
        Update the KL coefficient based on the observed KL divergence.

        Parameters
        ----------
        current_kl : float
            The KL divergence observed in the last batch.
        n_steps : int
            Number of steps since the last update.

        Returns
        -------
        float
            The updated KL coefficient.
        """
        # Only update if enough steps have passed
        if n_steps < self.horizon:
            return self.kl_coef

        # Compute the adjustment factor
        if self.target_kl == 0:
            # Avoid division by zero; if target is zero, keep coefficient unchanged
            return self.kl_coef

        ratio = (current_kl - self.target_kl) / self.target_kl
        new_coef = self.kl_coef * math.exp(ratio)

        # Clamp to a reasonable range to avoid numerical issues
        new_coef = max(0.0, min(new_coef, 1e6))

        self.kl_coef = new_coef
        return self.kl_coef