def add_fourier_features(inputs: torch.Tensor, start=6, stop=8, step=1):
    import torch
    import numpy as np
    
    # Generate the frequency bands
    freqs = np.arange(start, stop, step)
    
    # Create a list to store all features
    features = [inputs]
    
    # For each frequency, create sin and cos features
    for freq in freqs:
        # Calculate the frequency scaling factor (2^freq)
        freq_scale = 2 ** freq
        
        # Add sin and cos features
        features.append(torch.sin(freq_scale * np.pi * inputs))
        features.append(torch.cos(freq_scale * np.pi * inputs))
    
    # Concatenate all features along the last dimension
    return torch.cat(features, dim=-1)