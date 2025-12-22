def broadcast_params(module):
    """
    Recursively broadcasts the parameters of a PyTorch module to all its child modules.

    Args:
        module (torch.nn.Module): The module whose parameters need to be broadcasted.

    Returns:
        None
    """
    for param in module.parameters():
        param.data = param.data.clone().detach()

    for child_module in module.children():
        broadcast_params(child_module)