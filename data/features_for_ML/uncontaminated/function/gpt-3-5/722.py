def log_norm(x, mean=-4, std=4, dim=2):
    import torch
    import torch.nn.functional as F
    
    mel = torch.exp(x)
    norm_mel = (mel - mean) / std
    log_norm_mel = torch.log(F.relu(norm_mel) + 1e-6)
    
    return log_norm_mel, norm_mel, mel