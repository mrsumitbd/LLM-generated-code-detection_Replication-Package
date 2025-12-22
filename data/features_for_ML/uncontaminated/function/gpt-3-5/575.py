import numpy as np

def measure_slopes_at_exposure(log_exposure, density_curves, 
                               log_exposure_reference=0.0,
                               log_exposure_range=np.log10(2**2)):
    
    def calculate_slope(x1, y1, x2, y2):
        return (y2 - y1) / (x2 - x1)
    
    slopes = []
    for curve in density_curves:
        idx = np.abs(log_exposure - log_exposure_reference) <= log_exposure_range
        x1 = log_exposure[idx][0]
        y1 = curve[idx][0]
        x2 = log_exposure[idx][-1]
        y2 = curve[idx][-1]
        slope = calculate_slope(x1, y1, x2, y2)
        slopes.append(slope)
    
    return slopes