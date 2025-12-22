import numpy as np

def residual_simple(params, wl, cmy_model, data, dstm, paper_sens, log_exposure, density_curves, model='model_a', biases=(1,2,2)):
    """
    Calculates the residual between the predicted and measured color densities.

    Args:
        params (tuple): A tuple of parameters for the color model.
        wl (numpy.ndarray): An array of wavelengths.
        cmy_model (callable): A function that calculates the CMY densities given the parameters and wavelengths.
        data (numpy.ndarray): An array of measured color densities.
        dstm (numpy.ndarray): An array of paper sensitivities.
        paper_sens (numpy.ndarray): An array of paper sensitivities.
        log_exposure (float): The log exposure value.
        density_curves (numpy.ndarray): An array of density curves.
        model (str, optional): The color model to use, either 'model_a' or 'model_b'. Defaults to 'model_a'.
        biases (tuple, optional): A tuple of bias values for the color channels. Defaults to (1, 2, 2).

    Returns:
        numpy.ndarray: An array of residuals between the predicted and measured color densities.
    """
    if model == 'model_a':
        cmy = cmy_model(params, wl)
    else:
        cmy = cmy_model(params, wl, dstm)

    cmy = np.clip(cmy, 0, None)
    predicted = np.exp(-cmy * biases)
    residual = data - predicted
    return residual