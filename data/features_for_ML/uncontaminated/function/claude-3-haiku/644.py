def full_load_to_vram(self) -> int:
    """Load all weights into VRAM (if supported by the model).
    Returns:
        The number of bytes loaded into VRAM.
    """
    total_bytes_loaded = 0
    for parameter in self.parameters():
        bytes_loaded = self._load_parameter_to_vram(parameter)
        total_bytes_loaded += bytes_loaded
    return total_bytes_loaded

def _load_parameter_to_vram(self, parameter: torch.Tensor) -> int:
    """Load a single parameter tensor into VRAM."""
    device = torch.device("cuda")
    parameter.to(device)
    return parameter.element_size() * parameter.numel()