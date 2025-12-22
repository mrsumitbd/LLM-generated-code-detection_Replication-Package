import torch
import numpy as np
import numpy.typing as npt

def prepare_probe_features(
    features: npt.NDArray[np.float32] | npt.NDArray[np.float64] | torch.Tensor,
) -> torch.Tensor:
    if isinstance(features, np.ndarray):
        features = torch.from_numpy(features)
    
    if features.ndim == 1:
        raise ValueError("Invalid shape: Single summary vector")
    elif features.ndim == 2 and features.shape[0] == 4:
        return features.unsqueeze(0)
    elif features.ndim == 2 and features.shape[1] == 4:
        return features
    elif features.ndim == 2 and features.shape[1] == 128:
        return features
    elif features.ndim == 3 and features.shape[1] == 4:
        return features
    elif features.ndim == 3 and features.shape[2] == 128:
        return features
    else:
        raise ValueError("Invalid shape: Invalid input shape")