import torch

def center_size(boxes):
    """
    Convert point_form boxes (xmin, ymin, xmax, ymax) to center_size form (cx, cy, w, h).

    Args:
        boxes (torch.Tensor): Tensor of shape (..., 4) in point_form.

    Returns:
        torch.Tensor: Tensor of shape (..., 4) in center_size form.
    """
    # Ensure boxes is a torch tensor
    if not isinstance(boxes, torch.Tensor):
        boxes = torch.tensor(boxes, dtype=torch.float32)

    xmin = boxes[..., 0]
    ymin = boxes[..., 1]
    xmax = boxes[..., 2]
    ymax = boxes[..., 3]

    cx = (xmin + xmax) / 2.0
    cy = (ymin + ymax) / 2.0
    w  = xmax - xmin
    h  = ymax - ymin

    return torch.stack((cx, cy, w, h), dim=-1)