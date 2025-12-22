class MultiOptimizer:

    def __init__(self, optimizers={}, schedulers={}):
        self.optimizers = optimizers
        self.schedulers = schedulers

    def state_dict(self):
        return {key: optimizer.state_dict() for key, optimizer in self.optimizers.items()}

    def scheduler_state_dict(self):
        return {key: scheduler.state_dict() for key, scheduler in self.schedulers.items()}

    def load_state_dict(self, state_dict):
        for key, optimizer_state in state_dict.items():
            self.optimizers[key].load_state_dict(optimizer_state)

    def load_scheduler_state_dict(self, state_dict):
        for key, scheduler_state in state_dict.items():
            self.schedulers[key].load_state_dict(scheduler_state)

    def step(self, key=None, scaler=None):
        if key is None:
            for key in self.optimizers.keys():
                self._step(key, scaler)
        else:
            self._step(key, scaler)

    def _step(self, key, scaler=None):
        self.optimizers[key].step(scaler)

    def zero_grad(self, key=None):
        if key is None:
            for key in self.optimizers.keys():
                self.optimizers[key].zero_grad()
        else:
            self.optimizers[key].zero_grad()

    def scheduler(self, *args, key=None):
        if key is None:
            for key in self.schedulers.keys():
                self.schedulers[key](*args)
        else:
            self.schedulers[key](*args)