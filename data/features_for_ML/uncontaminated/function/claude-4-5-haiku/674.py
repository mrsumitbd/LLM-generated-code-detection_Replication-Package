def _compute_mean_and_conf_int(val):
    import numpy as np
    from scipy import stats
    
    val = np.asarray(val)
    n = len(val)
    
    if n == 0:
        return np.nan, np.nan, np.nan
    
    mean = np.mean(val)
    
    if n == 1:
        return mean, np.nan, np.nan
    
    std_err = stats.sem(val)
    ci = std_err * stats.t.ppf((1 + 0.95) / 2, n - 1)
    
    return mean, mean - ci, mean + ci