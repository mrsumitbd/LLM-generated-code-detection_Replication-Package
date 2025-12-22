class MultiOptimizer:
    def __init__(self, optimizers={}, schedulers={}):
        self.optimizers = optimizers
        self.schedulers = schedulers

    def state_dict(self):
        state_dict = {}
        for key, optimizer in self.optimizers.items():
            state_dict[key] = optimizer.state_dict()
        return state_dict

    def scheduler_state_dict(self):
        scheduler_state_dict = {}
        for key, scheduler in self.schedulers.items():
            scheduler_state_dict[key] = scheduler.state_dict()
        return scheduler_state_dict

    def load_state_dict(self, state_dict):
        for key, optimizer_state in state_dict.items():
            self.optimizers[key].load_state_dict(optimizer_state)

    def load_scheduler_state_dict(self, state_dict):
        for key, scheduler_state in state_dict.items():
            self.schedulers[key].load_state_dict(scheduler_state)

    def step(self, key=None, scaler=None):
        if key is None:
            for k, optimizer in self.optimizers.items():
                self._step(k, scaler)
        else:
            self._step(key, scaler)

    def _step(self, key, scaler=None):
        self.optimizers[key].step()
        if key in self.schedulers:
            self.schedulers[key].step()

    def zero_grad(self, key=None):
        if key is None:
            for optimizer in self.optimizers.values():
                optimizer.zero_grad()
        else:
            self.optimizers[key].zero_grad()

    def scheduler(self, *args, key=None):
        if key is None:
            for scheduler in self.schedulers.values():
                scheduler.step(*args)
        else:
            self.schedulers[key].step(*args)