def full_load_to_vram(self) -> int:
    total_bytes = 0
    for param in self.parameters():
        if param.requires_grad:
            param_data = param.data
            if param_data.is_cuda:
                total_bytes += param_data.element_size() * param_data.nelement()
    return total_bytes