import time
import os
import functools
import statistics

class ContextualAutoTuner:
    """
    A simple auto‑tuner that measures the execution time of a function.
    It performs a number of warm‑up runs followed by a number of timed runs.
    The average and standard deviation of the timed runs are printed.
    If `is_dist` is True, printing is suppressed on all ranks except rank 0.
    """

    def __init__(self, fn, is_dist=False, n_repeat=5, n_warmup=3):
        """
        Parameters
        ----------
        fn : callable
            The function to be timed.
        is_dist : bool, optional
            If True, suppress printing on non‑zero ranks.
        n_repeat : int, optional
            Number of timed repetitions.
        n_warmup : int, optional
            Number of warm‑up repetitions (not timed).
        """
        self.fn = fn
        self.is_dist = is_dist
        self.n_repeat = n_repeat
        self.n_warmup = n_warmup

    def dist_print(self, *args, **kwargs):
        """
        Print only on rank 0 when distributed.
        """
        if self.is_dist:
            rank = int(os.environ.get("RANK", "0"))
            if rank != 0:
                return
        print(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Execute the wrapped function with warm‑up and timed runs.
        Returns the result of the last call.
        """
        # Warm‑up runs (not timed)
        for _ in range(self.n_warmup):
            self.fn(*args, **kwargs)

        # Timed runs
        times = []
        result = None
        for _ in range(self.n_repeat):
            start = time.perf_counter()
            result = self.fn(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)

        avg_time = statistics.mean(times)
        std_time = statistics.stdev(times) if len(times) > 1 else 0.0

        self.dist_print(
            f"[AutoTuner] Function '{self.fn.__name__}' "
            f"timed over {self.n_repeat} runs: "
            f"avg={avg_time:.6f}s, std={std_time:.6f}s"
        )

        return result