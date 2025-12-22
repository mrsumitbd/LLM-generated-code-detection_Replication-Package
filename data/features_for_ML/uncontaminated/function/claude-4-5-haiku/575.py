def measure_slopes_at_exposure(log_exposure, density_curves, 
                               log_exposure_reference=0.0,
                               log_exposure_range=np.log10(2**2)):
    """
    Measure the slopes of density curves at a specific exposure level.
    
    Parameters:
    -----------
    log_exposure : array-like
        Log10 of exposure values
    density_curves : array-like
        Density values corresponding to log_exposure, shape (n_curves, len(log_exposure))
    log_exposure_reference : float
        The reference log exposure at which to measure slopes
    log_exposure_range : float
        The range around the reference exposure to use for slope calculation
    
    Returns:
    --------
    slopes : ndarray
        Array of slopes measured at the reference exposure for each curve
    """
    slopes = []
    
    # Calculate the bounds for the exposure range
    lower_bound = log_exposure_reference - log_exposure_range / 2
    upper_bound = log_exposure_reference + log_exposure_range / 2
    
    # Find indices within the range
    mask = (log_exposure >= lower_bound) & (log_exposure <= upper_bound)
    indices = np.where(mask)[0]
    
    if len(indices) < 2:
        # Not enough points to calculate slope
        return np.zeros(len(density_curves))
    
    # Extract the subset of log_exposure values
    x_subset = log_exposure[indices]
    
    # Calculate slope for each density curve
    for curve in density_curves:
        y_subset = curve[indices]
        
        # Use linear regression to find the slope
        coefficients = np.polyfit(x_subset, y_subset, 1)
        slope = coefficients[0]
        slopes.append(slope)
    
    return np.array(slopes)