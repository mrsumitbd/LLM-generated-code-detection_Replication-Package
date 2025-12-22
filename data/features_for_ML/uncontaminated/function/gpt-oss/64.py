import numpy as np
from math import gcd
try:
    from scipy.signal import resample_poly
except ImportError:
    resample_poly = None

def audio_resample(data, config: 'DataConfig'):
    """
    Resample audio data in place.

    Parameters
    ----------
    data : np.ndarray
        Audio samples. Shape (n_samples,) or (n_samples, n_channels).
    config : DataConfig
        Configuration object with at least the following attributes:
        - sample_rate : int
            Original sampling rate.
        - target_sample_rate : int
            Desired sampling rate.
        - resample_method : str, optional
            Method to use for resampling. Supported values:
            - 'poly' (default): use scipy.signal.resample_poly
            - 'linear': use linear interpolation via np.interp
            - 'sinc': use scipy.signal.resample (requires scipy)
    """
    # Validate input
    if not isinstance(data, np.ndarray):
        raise TypeError("data must be a numpy array")
    if not hasattr(config, 'sample_rate') or not hasattr(config, 'target_sample_rate'):
        raise AttributeError("config must have sample_rate and target_sample_rate attributes")

    src_sr = int(config.sample_rate)
    dst_sr = int(config.target_sample_rate)

    if src_sr == dst_sr:
        return  # nothing to do

    method = getattr(config, 'resample_method', 'poly').lower()

    # Helper to reshape data for 1D case
    if data.ndim == 1:
        data = data[:, None]  # make it 2D for uniform processing
        single_channel = True
    else:
        single_channel = False

    # Resample
    if method == 'poly':
        if resample_poly is None:
            raise RuntimeError("scipy.signal.resample_poly is required for 'poly' method")
        # Compute up/down factors
        up = dst_sr
        down = src_sr
        g = gcd(up, down)
        up //= g
        down //= g
        resampled = resample_poly(data, up, down, axis=0)
    elif method == 'linear':
        # Linear interpolation
        n_orig = data.shape[0]
        n_new = int(np.round(n_orig * dst_sr / src_sr))
        x_orig = np.arange(n_orig)
        x_new = np.linspace(0, n_orig - 1, n_new)
        resampled = np.empty((n_new, data.shape[1]), dtype=data.dtype)
        for ch in range(data.shape[1]):
            resampled[:, ch] = np.interp(x_new, x_orig, data[:, ch])
    elif method == 'sinc':
        try:
            from scipy.signal import resample
        except ImportError:
            raise RuntimeError("scipy.signal.resample is required for 'sinc' method")
        n_new = int(np.round(data.shape[0] * dst_sr / src_sr))
        resampled = resample(data, n_new, axis=0)
    else:
        raise ValueError(f"Unsupported resample_method: {method}")

    # In-place update
    if resampled.shape == data.shape:
        data[:] = resampled
    else:
        # If shapes differ, we cannot truly do in-place; replace contents up to min size
        min_rows = min(data.shape[0], resampled.shape[0])
        data[:min_rows, :] = resampled[:min_rows, :]
        # If new data has more rows, we cannot add them in-place; raise warning
        if resampled.shape[0] > data.shape[0]:
            raise RuntimeError("Resampled data has more samples than original; cannot replace in-place")

    # If original data was 1D, reshape back
    if single_channel:
        data.resize(resampled.shape[0])