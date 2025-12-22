import numpy as np

def measure_slopes_at_exposure(log_exposure, density_curves, 
                               log_exposure_reference=0.0,
                               log_exposure_range=np.log10(2**2)):
    """
    Measure the slopes of the density curves at the specified log exposure.

    Args:
        log_exposure (float): The log exposure value at which to measure the slopes.
        density_curves (numpy.ndarray): A 2D array of density values, where each row represents a density curve.
        log_exposure_reference (float, optional): The reference log exposure value. Defaults to 0.0.
        log_exposure_range (float, optional): The range of log exposure values to consider. Defaults to np.log10(2**2).

    Returns:
        numpy.ndarray: A 1D array of slope values, one for each density curve.
    """
    # Compute the index of the reference log exposure
    ref_idx = np.argmin(np.abs(log_exposure - log_exposure_reference))

    # Compute the indices of the log exposure range
    start_idx = np.argmin(np.abs(log_exposure - (log_exposure_reference - log_exposure_range/2)))
    end_idx = np.argmin(np.abs(log_exposure - (log_exposure_reference + log_exposure_range/2)))

    # Compute the slopes at the specified log exposure
    slopes = (density_curves[:, end_idx] - density_curves[:, start_idx]) / (log_exposure[end_idx] - log_exposure[start_idx])

    return slopes