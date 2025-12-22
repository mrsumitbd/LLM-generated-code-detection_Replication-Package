import numpy as np
from scipy.optimize import minimize
import json

def residual_simple(params, wl, cmy_model, data, dstm, paper_sens, log_exposure, density_curves, model='model_a', biases=(1,2,2)):
    """
    Calculate residuals for color model fitting.
    
    Args:
        params: Model parameters to optimize
        wl: Wavelengths
        cmy_model: CMY model function
        data: Observed data
        dstm: Density to spectral model
        paper_sens: Paper sensitivity
        log_exposure: Log exposure values
        density_curves: Density curves for CMY
        model: Model type ('model_a' or 'model_b')
        biases: Bias weights for different components
    
    Returns:
        Residuals (differences between predicted and observed data)
    """
    try:
        # Unpack parameters based on model type
        if model == 'model_a':
            # Model A parameters
            if len(params) >= 3:
                c_param, m_param, y_param = params[:3]
            else:
                return np.full_like(data, 1e10)
        elif model == 'model_b':
            # Model B parameters
            if len(params) >= 6:
                c_param, m_param, y_param = params[:3]
                c_scale, m_scale, y_scale = params[3:6]
            else:
                return np.full_like(data, 1e10)
        else:
            return np.full_like(data, 1e10)
        
        # Ensure parameters are within reasonable bounds
        params_bounded = np.clip(params, -10, 10)
        
        # Generate predicted data using the CMY model
        predicted = cmy_model(
            params_bounded,
            wl=wl,
            dstm=dstm,
            paper_sens=paper_sens,
            log_exposure=log_exposure,
            density_curves=density_curves
        )
        
        # Calculate residuals with bias weighting
        if len(data) == len(predicted):
            residuals = (data - predicted) * np.array(biases)
        else:
            # Handle dimension mismatch
            min_len = min(len(data), len(predicted))
            residuals = np.zeros_like(data)
            residuals[:min_len] = (data[:min_len] - predicted[:min_len]) * np.array(biases)
            residuals[min_len:] = data[min_len:] * np.array(biases)[0]
        
        return residuals
    
    except Exception as e:
        # Return large residuals on error
        return np.full_like(data, 1e10)