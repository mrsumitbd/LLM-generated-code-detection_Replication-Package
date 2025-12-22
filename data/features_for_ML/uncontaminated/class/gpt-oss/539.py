class AverageMeter:
    """
    Computes and stores the average and current value.
    Useful for tracking metrics during training or evaluation.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset all statistics."""
        self.val = 0.0   # most recent value
        self.avg = 0.0   # running average
        self.sum = 0.0   # cumulative sum
        self.count = 0   # number of updates

    def update(self, val, n=1):
        """
        Update the meter with a new value.

        Args:
            val (float): New value to incorporate.
            n (int, optional): Weight of the new value (default: 1).
        """
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count if self.count != 0 else 0.0