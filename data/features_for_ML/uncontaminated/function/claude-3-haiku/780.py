import torch

def compute_errors_torch(gt, pred):
    """
    Computes various error metrics between ground truth and predicted tensors.
    
    Args:
        gt (torch.Tensor): Ground truth tensor.
        pred (torch.Tensor): Predicted tensor.
        
    Returns:
        dict: A dictionary containing the following error metrics:
            - 'mse': Mean Squared Error
            - 'rmse': Root Mean Squared Error
            - 'mae': Mean Absolute Error
            - 'psnr': Peak Signal-to-Noise Ratio
    """
    mse = torch.mean((gt - pred) ** 2)
    rmse = torch.sqrt(mse)
    mae = torch.mean(torch.abs(gt - pred))
    
    # Compute PSNR
    max_val = torch.max(gt)
    psnr = 20 * torch.log10(max_val / rmse)
    
    return {'mse': mse.item(), 'rmse': rmse.item(), 'mae': mae.item(), 'psnr': psnr.item()}