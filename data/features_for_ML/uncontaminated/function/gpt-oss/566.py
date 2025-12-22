import torch

def tensor2mask(t: torch.Tensor) -> torch.Tensor:
    """
    Convert a tensor of class scores or probabilities into a mask of class indices.
    
    Parameters
    ----------
    t : torch.Tensor
        Tensor containing class scores/probabilities. Expected shapes:
        - (N, C, H, W) -> returns (N, H, W)
        - (C, H, W)   -> returns (H, W)
        - (C, H, W, ...) -> returns (..., H, W) with argmax over the first dimension
        - (C,)        -> returns scalar index
        - (N, C)      -> returns (N,)
    
    Returns
    -------
    torch.Tensor
        Mask tensor with the same spatial dimensions as the input but with a single
        channel containing the class index (dtype=torch.long).
    """
    # Determine the dimension to argmax over
    if t.dim() == 4:
        # (N, C, H, W) -> argmax over channel dim=1
        return t.argmax(dim=1)
    elif t.dim() == 3:
        # (C, H, W) -> argmax over channel dim=0
        return t.argmax(dim=0)
    elif t.dim() == 2:
        # (C, N) or (N, C) -> argmax over channel dim=0 or 1
        # We assume the first dimension is channel if it has more than 1 element
        if t.size(0) > 1:
            return t.argmax(dim=0)
        else:
            return t.argmax(dim=1)
    elif t.dim() == 1:
        # (C,) -> single index
        return t.argmax()
    else:
        # For any other shape, try to argmax over the first dimension
        return t.argmax(dim=0)