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
        state_dict = {}
        for key, scheduler in self.schedulers.items():
            state_dict[key] = scheduler.state_dict()
        return state_dict

    def load_state_dict(self, state_dict):
        for key, opt_state in state_dict.items():
            if key in self.optimizers:
                self.optimizers[key].load_state_dict(opt_state)

    def load_scheduler_state_dict(self, state_dict):
        for key, sched_state in state_dict.items():
            if key in self.schedulers:
                self.schedulers[key].load_state_dict(sched_state)

    def step(self, key=None, scaler=None):
        if key is None:
            for k in self.optimizers.keys():
                self._step(k, scaler)
        else:
            self._step(key, scaler)

    def _step(self, key, scaler=None):
        if key in self.optimizers:
            if scaler is not None:
                scaler.step(self.optimizers[key])
            else:
                self.optimizers[key].step()

    def zero_grad(self, key=None):
        if key is None:
            for optimizer in self.optimizers.values():
                optimizer.zero_grad()
        else:
            if key in self.optimizers:
                self.optimizers[key].zero_grad()

    def scheduler(self, *args, key=None):
        if key is None:
            for scheduler in self.schedulers.values():
                scheduler.step(*args)
        else:
            if key in self.schedulers:
                self.schedulers[key].step(*args)