def compute_errors_torch(gt, pred):
    import torch
    gt = torch.tensor(gt)
    pred = torch.tensor(pred)
    abs_diff = torch.abs(gt - pred)
    mse = torch.mean(abs_diff ** 2)
    rmse = torch.sqrt(mse)
    mae = torch.mean(abs_diff)
    return mse.item(), rmse.item(), mae.item()