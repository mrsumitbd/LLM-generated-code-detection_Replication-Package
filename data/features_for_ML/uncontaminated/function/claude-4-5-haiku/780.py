import torch
import torch.nn.functional as F

def compute_errors_torch(gt, pred):
    """
    Compute various error metrics between ground truth and predictions using PyTorch.
    
    Args:
        gt: Ground truth tensor
        pred: Prediction tensor
    
    Returns:
        Dictionary containing various error metrics
    """
    # Ensure inputs are tensors
    if not isinstance(gt, torch.Tensor):
        gt = torch.tensor(gt, dtype=torch.float32)
    if not isinstance(pred, torch.Tensor):
        pred = torch.tensor(pred, dtype=torch.float32)
    
    # Ensure same shape
    if gt.shape != pred.shape:
        raise ValueError(f"Shape mismatch: gt {gt.shape} vs pred {pred.shape}")
    
    # Compute various error metrics
    errors = {}
    
    # Mean Absolute Error (MAE)
    errors['mae'] = torch.mean(torch.abs(gt - pred)).item()
    
    # Mean Squared Error (MSE)
    errors['mse'] = torch.mean((gt - pred) ** 2).item()
    
    # Root Mean Squared Error (RMSE)
    errors['rmse'] = torch.sqrt(torch.mean((gt - pred) ** 2)).item()
    
    # Mean Absolute Percentage Error (MAPE)
    # Avoid division by zero
    mask = gt != 0
    if torch.any(mask):
        mape = torch.mean(torch.abs((gt[mask] - pred[mask]) / gt[mask])) * 100
        errors['mape'] = mape.item()
    else:
        errors['mape'] = float('inf')
    
    # R-squared (coefficient of determination)
    ss_res = torch.sum((gt - pred) ** 2)
    ss_tot = torch.sum((gt - torch.mean(gt)) ** 2)
    if ss_tot != 0:
        errors['r2'] = (1 - ss_res / ss_tot).item()
    else:
        errors['r2'] = float('nan')
    
    # Correlation coefficient
    gt_mean = torch.mean(gt)
    pred_mean = torch.mean(pred)
    numerator = torch.sum((gt - gt_mean) * (pred - pred_mean))
    denominator = torch.sqrt(torch.sum((gt - gt_mean) ** 2) * torch.sum((pred - pred_mean) ** 2))
    if denominator != 0:
        errors['correlation'] = (numerator / denominator).item()
    else:
        errors['correlation'] = float('nan')
    
    return errors