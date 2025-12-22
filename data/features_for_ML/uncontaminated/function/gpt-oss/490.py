import torch
from torch import nn

def convert_module_to_f16(l):
    """
    Convert primitive modules to float16.

    Parameters
    ----------
    l : torch.nn.Module or iterable of torch.nn.Module
        The module(s) to convert. If an iterable is provided, each element
        will be processed recursively.

    Returns
    -------
    torch.nn.Module or list of torch.nn.Module
        The same module(s) with all parameters and buffers converted to
        torch.float16. The original object(s) are modified in-place.
    """
    # Helper to convert a single module
    def _convert(m: nn.Module):
        # Convert all parameters and buffers to float16
        for p in m.parameters():
            if p.dtype != torch.float16:
                p.data = p.data.half()
        for buf_name, buf in m.named_buffers():
            if buf.dtype != torch.float16:
                m._buffers[buf_name] = buf.half()

    # If l is an iterable of modules (but not a string or bytes)
    if isinstance(l, (list, tuple)):
        for sub in l:
            if isinstance(sub, nn.Module):
                _convert(sub)
                # Recursively convert submodules
                for subsub in sub.modules():
                    if subsub is not sub:
                        _convert(subsub)
        return l

    # If l is a single module
    if isinstance(l, nn.Module):
        _convert(l)
        for sub in l.modules():
            if sub is not l:
                _convert(sub)
        return l

    # Unsupported type: return as is
    return l