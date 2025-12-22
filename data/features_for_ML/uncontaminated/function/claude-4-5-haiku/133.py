def sinc(x: torch.Tensor):
    """
    Implementation of sinc, i.e. sin(pi * x) / (pi * x)
    __Warning__: Different to julius.sinc, the input is multiplied by `pi`!
    """
    pi_x = torch.tensor(torch.pi) * x
    return torch.sinc(pi_x / torch.tensor(torch.pi))