import numpy as np

def measure_slopes_at_exposure(log_exposure, density_curves,
                               log_exposure_reference=0.0,
                               log_exposure_range=np.log10(2**2)):
    """
    Estimate the slope of each density curve with respect to log exposure
    around a specified reference exposure.

    Parameters
    ----------
    log_exposure : array_like
        1‑D array of log10(exposure) values corresponding to the columns of
        ``density_curves``.
    density_curves : array_like
        2‑D array of shape (n_curves, n_exposures) containing the density
        values for each curve at the exposures given in ``log_exposure``.
    log_exposure_reference : float, optional
        The log10(exposure) value around which the slope is estimated.
    log_exposure_range : float, optional
        The total width (in log10 units) of the window around
        ``log_exposure_reference`` used for the linear fit.

    Returns
    -------
    slopes : ndarray
        1‑D array of length ``n_curves`` containing the estimated slope
        (Δdensity / Δlog_exposure) for each curve.  If a curve has fewer
        than two points within the fitting window, the corresponding slope
        is set to ``np.nan``.
    """
    log_exposure = np.asarray(log_exposure, dtype=float)
    density_curves = np.asarray(density_curves, dtype=float)

    if density_curves.ndim != 2:
        raise ValueError("density_curves must be a 2‑D array")

    n_curves, n_exposures = density_curves.shape
    if log_exposure.size != n_exposures:
        raise ValueError("log_exposure length must match the number of columns in density_curves")

    # Determine indices within the fitting window
    half_range = log_exposure_range / 2.0
    lower = log_exposure_reference - half_range
    upper = log_exposure_reference + half_range
    mask = (log_exposure >= lower) & (log_exposure <= upper)

    # If no points in window, return NaNs
    if not np.any(mask):
        return np.full(n_curves, np.nan, dtype=float)

    # Extract the relevant exposure values once
    x_fit = log_exposure[mask]

    slopes = np.empty(n_curves, dtype=float)
    slopes.fill(np.nan)

    # Fit a line to each curve within the window
    for i in range(n_curves):
        y_fit = density_curves[i, mask]
        if y_fit.size < 2:
            continue  # insufficient points
        # Linear regression: slope = cov(x,y)/var(x)
        cov_xy = np.cov(x_fit, y_fit, bias=True)[0, 1]
        var_x = np.var(x_fit, ddof=0)
        if var_x == 0:
            continue
        slopes[i] = cov_xy / var_x

    return slopes