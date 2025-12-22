from dataclasses import dataclass
from typing import Optional

@dataclass
class DeviceInfo:
    """Simple representation of a compute device."""
    name: str
    type: str  # e.g., "cuda", "cpu"
    memory: int  # in bytes

def _get_cuda_device_info() -> Optional[DeviceInfo]:
    try:
        import torch
    except Exception:
        return None

    if not torch.cuda.is_available():
        return None

    # Find the CUDA device with the most memory
    best_idx = 0
    best_mem = 0
    for idx in range(torch.cuda.device_count()):
        props = torch.cuda.get_device_properties(idx)
        if props.total_memory > best_mem:
            best_mem = props.total_memory
            best_idx = idx

    props = torch.cuda.get_device_properties(best_idx)
    return DeviceInfo(
        name=props.name,
        type="cuda",
        memory=props.total_memory,
    )

def _get_cpu_device_info() -> DeviceInfo:
    # On most systems we can approximate CPU memory as the total system memory
    try:
        import psutil
        mem = psutil.virtual_memory().total
    except Exception:
        mem = 0
    return DeviceInfo(name="CPU", type="cpu", memory=mem)

def get_optimal_device() -> DeviceInfo:
    """
    Return the most capable device available on the system.
    Prefer CUDA GPUs over CPU. If no CUDA device is available,
    fall back to CPU.
    """
    cuda_info = _get_cuda_device_info()
    if cuda_info is not None:
        return cuda_info
    return _get_cpu_device_info()