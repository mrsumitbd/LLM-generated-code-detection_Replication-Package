import torch.nn as nn

def conv_bn_no_relu(inp, oup, stride):
    """
    Convolution followed by BatchNorm without an activation.

    Parameters
    ----------
    inp : int
        Number of input channels.
    oup : int
        Number of output channels.
    stride : int
        Stride for the convolution.

    Returns
    -------
    nn.Sequential
        A sequential container with Conv2d and BatchNorm2d.
    """
    return nn.Sequential(
        nn.Conv2d(inp, oup, kernel_size=3, stride=stride, padding=1, bias=False),
        nn.BatchNorm2d(oup)
    )