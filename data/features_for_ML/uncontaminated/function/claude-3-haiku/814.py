import numpy as np

def init_weights(m, mean=0.0, std=0.01):
    return np.random.normal(mean, std, size=m)