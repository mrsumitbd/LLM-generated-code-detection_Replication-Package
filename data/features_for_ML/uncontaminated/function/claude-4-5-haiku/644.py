def full_load_to_vram(self) -> int:
    """Load all weights into VRAM (if supported by the model).
    Returns:
        The number of bytes loaded into VRAM.
    """
    total_bytes = 0
    
    if not hasattr(self, 'model') or self.model is None:
        return 0
    
    try:
        import torch
        
        device = next(self.model.parameters()).device
        
        if not torch.cuda.is_available() or device.type != 'cuda':
            return 0
        
        for param in self.model.parameters():
            if param.device.type != 'cuda':
                param.data = param.data.to(device)
            total_bytes += param.data.element_size() * param.data.nelement()
        
        for buffer in self.model.buffers():
            if buffer.device.type != 'cuda':
                buffer.data = buffer.data.to(device)
            total_bytes += buffer.data.element_size() * buffer.data.nelement()
        
        torch.cuda.synchronize()
        
    except (ImportError, AttributeError, RuntimeError):
        return 0
    
    return total_bytes