import torch

def compute_errors_torch(gt, pred):
    abs_rel = torch.mean(torch.abs(gt - pred) / gt)
    return abs_rel