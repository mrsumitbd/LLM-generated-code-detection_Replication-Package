import numpy as np
from scipy.interpolate import interp1d, CubicSpline

def measure_slopes_at_exposure(log_exposure, density_curves, 
                               log_exposure_reference=0.0,
                               log_exposure_range=np.log10(2**2)):
    le_ref = log_exposure_reference
    log_exposure_0 = le_ref - log_exposure_range/2
    log_exposure_1 = le_ref + log_exposure_range/2
    gamma = np.zeros((3,))
    for i in range(3):
        sel = ~np.isnan(density_curves[:,i])
        density_1 = CubicSpline(log_exposure[sel], density_curves[sel,i])(log_exposure_1)
        density_0 = CubicSpline(log_exposure[sel], density_curves[sel,i])(log_exposure_0)
        gamma[i] = (density_1-density_0)/(log_exposure_1-log_exposure_0)
    return gamma