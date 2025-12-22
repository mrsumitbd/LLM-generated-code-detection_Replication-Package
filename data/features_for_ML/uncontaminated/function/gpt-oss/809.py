import numpy as np

def residual_simple(params, wl, cmy_model, data, dstm, paper_sens, log_exposure,
                    density_curves, model='model_a', biases=(1, 2, 2)):
    """
    Compute residuals between a model prediction and observed data.

    Parameters
    ----------
    params : array_like
        Parameters to be passed to the model function.
    wl : array_like
        Wavelengths at which the model is evaluated.
    cmy_model : callable
        Function that returns model predictions. It should accept at least
        ``params`` and ``wl`` as positional arguments. It may also accept
        optional keyword arguments: dstm, paper_sens, log_exposure,
        density_curves, model, biases.
    data : array_like
        Observed data to compare against the model predictions.
    dstm : dict or array_like
        Optional data structure used by the model.
    paper_sens : array_like
        Optional paper sensitivity curve used by the model.
    log_exposure : float
        Optional log exposure value used by the model.
    density_curves : dict or array_like
        Optional density curves used by the model.
    model : str, optional
        Model type identifier passed to the model function.
    biases : tuple, optional
        Bias factors applied to the model prediction (if supported by the
        model function).

    Returns
    -------
    residuals : ndarray
        The difference between the model prediction and the observed data.
        Shape matches that of ``data``.
    """
    # Ensure inputs are numpy arrays for broadcasting
    wl = np.asarray(wl, dtype=float)
    data = np.asarray(data, dtype=float)

    # Attempt to call the model with all optional arguments
    try:
        pred = cmy_model(params, wl,
                         dstm=dstm,
                         paper_sens=paper_sens,
                         log_exposure=log_exposure,
                         density_curves=density_curves,
                         model=model,
                         biases=biases)
    except TypeError:
        # Fallback: call with only required arguments
        pred = cmy_model(params, wl)

    # Convert prediction to numpy array
    pred = np.asarray(pred, dtype=float)

    # Broadcast if necessary
    if pred.shape != data.shape:
        try:
            pred = np.broadcast_to(pred, data.shape)
        except ValueError:
            raise ValueError("Shape mismatch between model prediction and data")

    # Compute residuals (model - data)
    residuals = pred - data

    return residuals