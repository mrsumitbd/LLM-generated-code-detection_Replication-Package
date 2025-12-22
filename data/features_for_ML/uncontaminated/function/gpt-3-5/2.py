import numpy as np

def rand_gumbel_like(x):
    return x - np.log(-np.log(np.random.rand(*x.shape)))