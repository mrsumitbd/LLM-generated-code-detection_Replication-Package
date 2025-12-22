import torch

def full_load_to_vram(self) -> int:
    """
    Load all weights into VRAM (if supported by the model).
    Returns:
        The number of bytes loaded into VRAM.
    """
    # Ensure we have a model and a CUDA device
    if not hasattr(self, "model") or self.model is None:
        return 0
    if not torch.cuda.is_available():
        return 0

    # Determine target device
    target_device = torch.device("cuda")
    if hasattr(self, "device") and isinstance(self.device, torch.device):
        target_device = self.device

    # Compute total bytes of all parameters
    total_bytes = 0
    for param in self.model.parameters():
        total_bytes += param.numel() * param.element_size()

    # Move all parameters to the target device
    try:
        self.model.to(target_device)
    except Exception:
        # If moving fails, return 0 bytes loaded
        return 0

    return total_bytes