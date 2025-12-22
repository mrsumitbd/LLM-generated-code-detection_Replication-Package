class MultiOptimizer:
    def __init__(self, optimizers=None, schedulers=None):
        """
        Parameters
        ----------
        optimizers : dict[str, torch.optim.Optimizer]
            Mapping from a key to an optimizer instance.
        schedulers : dict[str, torch.optim.lr_scheduler._LRScheduler]
            Mapping from a key to a scheduler instance.
        """
        self.optimizers = optimizers or {}
        self.schedulers = schedulers or {}

    def state_dict(self):
        """Return a dict mapping each key to the state dict of its optimizer."""
        return {k: opt.state_dict() for k, opt in self.optimizers.items()}

    def scheduler_state_dict(self):
        """Return a dict mapping each key to the state dict of its scheduler."""
        return {k: sch.state_dict() for k, sch in self.schedulers.items()}

    def load_state_dict(self, state_dict):
        """Load optimizer state dicts from a dict mapping keys to state dicts."""
        for k, sd in state_dict.items():
            if k in self.optimizers:
                self.optimizers[k].load_state_dict(sd)

    def load_scheduler_state_dict(self, state_dict):
        """Load scheduler state dicts from a dict mapping keys to state dicts."""
        for k, sd in state_dict.items():
            if k in self.schedulers:
                self.schedulers[k].load_state_dict(sd)

    def step(self, key=None, scaler=None):
        """
        Step all optimizers or a specific one.

        Parameters
        ----------
        key : str or None
            If None, step all optimizers. Otherwise step the optimizer with this key.
        scaler : torch.cuda.amp.GradScaler or None
            If provided, use scaler.step(optimizer) instead of optimizer.step().
        """
        if key is None:
            for k in self.optimizers:
                self._step(k, scaler=scaler)
        else:
            self._step(key, scaler=scaler)

    def _step(self, key, scaler=None):
        """Internal helper to step a single optimizer."""
        opt = self.optimizers[key]
        if scaler is not None:
            scaler.step(opt)
        else:
            opt.step()

    def zero_grad(self, key=None):
        """
        Zero gradients for all optimizers or a specific one.

        Parameters
        ----------
        key : str or None
            If None, zero all optimizers. Otherwise zero the optimizer with this key.
        """
        if key is None:
            for opt in self.optimizers.values():
                opt.zero_grad()
        else:
            self.optimizers[key].zero_grad()

    def scheduler(self, *args, key=None):
        """
        Return the scheduler for a given key or all schedulers.

        Parameters
        ----------
        key : str or None
            If None, return the entire scheduler dict. Otherwise return the scheduler
            associated with this key.
        """
        if key is None:
            return self.schedulers
        return self.schedulers[key]