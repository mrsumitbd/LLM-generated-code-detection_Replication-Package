import torch

def compute_errors_torch(gt: torch.Tensor, pred: torch.Tensor):
    """
    Compute common depth estimation error metrics between ground truth and prediction.

    Parameters
    ----------
    gt : torch.Tensor
        Ground‑truth depth map (float tensor).
    pred : torch.Tensor
        Predicted depth map (float tensor).

    Returns
    -------
    dict
        Dictionary containing the following keys:
        - abs_rel : Absolute relative difference
        - sq_rel  : Squared relative difference
        - rmse    : Root mean squared error
        - rmse_log: Root mean squared log error
        - a1      : Accuracy under threshold 1.25
        - a2      : Accuracy under threshold 1.25^2
        - a3      : Accuracy under threshold 1.25^3
    """
    # Ensure tensors are float
    gt = gt.float()
    pred = pred.float()

    # Valid mask: both gt and pred must be positive
    mask = (gt > 0) & (pred > 0)
    if mask.sum() == 0:
        # No valid pixels, return zeros
        return {
            'abs_rel': 0.0,
            'sq_rel': 0.0,
            'rmse': 0.0,
            'rmse_log': 0.0,
            'a1': 0.0,
            'a2': 0.0,
            'a3': 0.0,
        }

    gt = gt[mask]
    pred = pred[mask]

    # Absolute relative difference
    abs_rel = torch.mean(torch.abs(gt - pred) / gt)

    # Squared relative difference
    sq_rel = torch.mean((gt - pred) ** 2 / gt)

    # Root mean squared error
    rmse = torch.sqrt(torch.mean((gt - pred) ** 2))

    # Root mean squared log error
    rmse_log = torch.sqrt(torch.mean((torch.log(gt) - torch.log(pred)) ** 2))

    # Accuracy thresholds
    ratio = torch.max(gt / pred, pred / gt)
    a1 = torch.mean((ratio < 1.25).float())
    a2 = torch.mean((ratio < 1.25 ** 2).float())
    a3 = torch.mean((ratio < 1.25 ** 3).float())

    return {
        'abs_rel': abs_rel.item(),
        'sq_rel': sq_rel.item(),
        'rmse': rmse.item(),
        'rmse_log': rmse_log.item(),
        'a1': a1.item(),
        'a2': a2.item(),
        'a3': a3.item(),
    }