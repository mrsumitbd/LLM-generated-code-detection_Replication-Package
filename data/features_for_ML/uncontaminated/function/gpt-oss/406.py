import torch
from typing import Tuple, Any

def get_output_shape(module: torch.nn.Module, input_shape: Tuple[int, ...]) -> Tuple[int, ...]:
    """
    Calculates the output shape of a PyTorch module given an input shape.

    Args:
        module (nn.Module): a PyTorch module
        input_shape (tuple): A tuple representing the input shape, e.g., (batch_size, channels, height, width)

    Returns:
        tuple: The output shape of the module.
    """
    # Ensure the module is in evaluation mode
    was_training = module.training
    module.eval()

    # Create a dummy input tensor on CPU
    dummy_input = torch.randn(input_shape)

    with torch.no_grad():
        output = module(dummy_input)

    # Restore original training state
    module.train(was_training)

    # Helper to extract shape from various output types
    def _extract_shape(x: Any) -> Tuple[int, ...]:
        if isinstance(x, torch.Tensor):
            return tuple(x.shape)
        if isinstance(x, (list, tuple)):
            # Return shape of the first element
            return _extract_shape(x[0])
        if isinstance(x, dict):
            # Return shape of the first value
            return _extract_shape(next(iter(x.values())))
        # Fallback: return empty tuple
        return ()

    return _extract_shape(output)