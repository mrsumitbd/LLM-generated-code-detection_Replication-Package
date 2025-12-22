import torch

def get_output_shape(module: torch.nn.Module, input_shape: tuple) -> tuple:
    """
    Calculates the output shape of a PyTorch module given an input shape.

    Args:
        module (nn.Module): a PyTorch module
        input_shape (tuple): A tuple representing the input shape, e.g., (batch_size, channels, height, width)

    Returns:
        tuple: The output shape of the module.
    """
    # 获取模块的设备
    device = next(module.parameters()).device if list(module.parameters()) else torch.device('cpu')
    dummy_input = torch.zeros(size=input_shape, device=device)
    with torch.inference_mode():
        output = module(dummy_input)
    return tuple(output.shape)