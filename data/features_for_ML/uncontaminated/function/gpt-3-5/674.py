def _compute_mean_and_conf_int(val):
    import numpy as np
    mean = np.mean(val)
    std_dev = np.std(val)
    n = len(val)
    z = 1.96  # 95% confidence interval
    conf_int = z * (std_dev / (n ** 0.5))
    return mean, mean - conf_int, mean + conf_int