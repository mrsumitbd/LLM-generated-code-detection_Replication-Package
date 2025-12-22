def convert_module_to_f16(l):
    """
    Convert primitive modules to float16.
    """
    if isinstance(l, torch.nn.Module):
        if any(isinstance(p, torch.nn.Conv2d) or isinstance(p, torch.nn.Linear) for p in l.modules()):
            for param in l.parameters():
                param.data = param.data.half()
    elif isinstance(l, (list, tuple)):
        for item in l:
            convert_module_to_f16(item)
    return l