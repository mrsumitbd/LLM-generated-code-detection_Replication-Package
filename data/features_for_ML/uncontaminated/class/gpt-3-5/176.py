import time

class ContextualAutoTuner:

    def __init__(self, fn, is_dist=False, n_repeat=5, n_warmup=3):
        self.fn = fn
        self.is_dist = is_dist
        self.n_repeat = n_repeat
        self.n_warmup = n_warmup

    def dist_print(self, *args, **kwargs):
        if self.is_dist:
            print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        total_time = 0
        for _ in range(self.n_repeat + self.n_warmup):
            start_time = time.time()
            self.fn(*args, **kwargs)
            end_time = time.time()
            if self.n_warmup > 0:
                self.n_warmup -= 1
            else:
                total_time += end_time - start_time
        avg_time = total_time / self.n_repeat
        return avg_time