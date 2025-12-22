def get_output_shape(module: torch.nn.Module, input_shape: tuple) -> tuple:
    """
    Calculates the output shape of a PyTorch module given an input shape.

    Args:
        module (nn.Module): a PyTorch module
        input_shape (tuple): A tuple representing the input shape, e.g., (batch_size, channels, height, width)

    Returns:
        tuple: The output shape of the module.
    """
    input_tensor = torch.randn(input_shape)
    output_tensor = module(input_tensor)
    return output_tensor.shape