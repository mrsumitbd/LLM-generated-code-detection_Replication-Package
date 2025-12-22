def get_output_shape(module: torch.nn.Module, input_shape: tuple) -> tuple:
    with torch.no_grad():
        input_tensor = torch.randn(input_shape)
        output_tensor = module(input_tensor)
        return tuple(output_tensor.size())