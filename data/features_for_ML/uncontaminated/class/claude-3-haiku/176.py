import time
import numpy as np
from functools import wraps

class ContextualAutoTuner:
    def __init__(self, fn, is_dist=False, n_repeat=5, n_warmup=3):
        self.fn = fn
        self.is_dist = is_dist
        self.n_repeat = n_repeat
        self.n_warmup = n_warmup
        self.times = []

    def dist_print(self, *args, **kwargs):
        if self.is_dist:
            print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        self.times.clear()
        for _ in range(self.n_warmup):
            self.fn(*args, **kwargs)

        for _ in range(self.n_repeat):
            start_time = time.time()
            result = self.fn(*args, **kwargs)
            end_time = time.time()
            self.times.append(end_time - start_time)

        mean_time = np.mean(self.times)
        std_time = np.std(self.times)
        self.dist_print(f"Function took {mean_time:.6f} ± {std_time:.6f} seconds on average.")
        return result