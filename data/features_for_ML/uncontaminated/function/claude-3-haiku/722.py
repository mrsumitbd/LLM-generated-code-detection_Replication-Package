import numpy as np

def log_norm(x, mean=-4, std=4, dim=2):
    """
    normalized log mel -> mel -> norm -> log(norm)
    """
    x = np.log(x)
    x = (x - mean) / std
    x = np.exp(x)
    x = np.linalg.norm(x, axis=dim)
    x = np.log(x)
    return x