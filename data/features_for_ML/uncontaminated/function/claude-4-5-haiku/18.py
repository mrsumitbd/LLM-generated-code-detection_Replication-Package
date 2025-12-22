def get_optimal_device() -> DeviceInfo:
    import torch
    
    if torch.cuda.is_available():
        device_type = "cuda"
        device_index = torch.cuda.current_device()
        device_name = torch.cuda.get_device_name(device_index)
        device_capability = torch.cuda.get_device_capability(device_index)
        total_memory = torch.cuda.get_device_properties(device_index).total_memory
        
        return DeviceInfo(
            device_type=device_type,
            device_index=device_index,
            device_name=device_name,
            device_capability=device_capability,
            total_memory=total_memory,
            is_available=True
        )
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return DeviceInfo(
            device_type="mps",
            device_index=0,
            device_name="Apple Metal Performance Shaders",
            device_capability=None,
            total_memory=None,
            is_available=True
        )
    else:
        return DeviceInfo(
            device_type="cpu",
            device_index=0,
            device_name="CPU",
            device_capability=None,
            total_memory=None,
            is_available=True
        )