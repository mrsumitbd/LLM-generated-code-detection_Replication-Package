import torch

class CheckpointState:
    def __init__(self, model, optimizer, scheduler, epoch):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.epoch = epoch

    def save_checkpoint(self, filepath):
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'epoch': self.epoch
        }
        torch.save(checkpoint, filepath)

    @staticmethod
    def load_checkpoint(filepath):
        checkpoint = torch.load(filepath)
        model = checkpoint['model_state_dict']
        optimizer = checkpoint['optimizer_state_dict']
        scheduler = checkpoint['scheduler_state_dict']
        epoch = checkpoint['epoch']
        return CheckpointState(model, optimizer, scheduler, epoch)