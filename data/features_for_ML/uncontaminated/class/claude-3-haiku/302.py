class CheckpointState:
    """State of model, optimizer, and scheduler after a given number of epochs."""

    def __init__(self, model_state_dict, optimizer_state_dict, scheduler_state_dict, epoch, best_metric):
        self.model_state_dict = model_state_dict
        self.optimizer_state_dict = optimizer_state_dict
        self.scheduler_state_dict = scheduler_state_dict
        self.epoch = epoch
        self.best_metric = best_metric

    def load_state_dict(self, model, optimizer, scheduler):
        model.load_state_dict(self.model_state_dict)
        optimizer.load_state_dict(self.optimizer_state_dict)
        scheduler.load_state_dict(self.scheduler_state_dict)

    def __str__(self):
        return f"CheckpointState(epoch={self.epoch}, best_metric={self.best_metric})"

    def __repr__(self):
        return str(self)