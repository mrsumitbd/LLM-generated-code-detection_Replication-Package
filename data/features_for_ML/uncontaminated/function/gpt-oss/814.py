import torch.nn as nn
import torch.nn.init as init

def init_weights(m, mean=0.0, std=0.01):
    """
    Initialize weights of a PyTorch module `m` using a normal distribution
    with the specified mean and standard deviation. Biases are set to zero.
    The function is intended to be used with `model.apply(init_weights)`.

    Parameters
    ----------
    m : nn.Module
        The module whose parameters will be initialized.
    mean : float, optional
        Mean of the normal distribution. Default is 0.0.
    std : float, optional
        Standard deviation of the normal distribution. Default is 0.01.
    """
    # Linear layers
    if isinstance(m, nn.Linear):
        init.normal_(m.weight, mean=mean, std=std)
        if m.bias is not None:
            init.constant_(m.bias, 0.0)

    # Convolutional layers
    elif isinstance(m, (nn.Conv1d, nn.Conv2d, nn.Conv3d,
                        nn.ConvTranspose1d, nn.ConvTranspose2d, nn.ConvTranspose3d)):
        init.normal_(m.weight, mean=mean, std=std)
        if m.bias is not None:
            init.constant_(m.bias, 0.0)

    # BatchNorm layers
    elif isinstance(m, (nn.BatchNorm1d, nn.BatchNorm2d, nn.BatchNorm3d,
                        nn.GroupNorm, nn.LayerNorm)):
        if hasattr(m, 'weight') and m.weight is not None:
            init.constant_(m.weight, 1.0)
        if hasattr(m, 'bias') and m.bias is not None:
            init.constant_(m.bias, 0.0)

    # Embedding layers
    elif isinstance(m, nn.Embedding):
        init.normal_(m.weight, mean=mean, std=std)