import numpy as np
from functools import partial
from concurrent.futures import ProcessPoolExecutor

class PotentialOps:
    """Mixin providing operations for potential functions:

    1. Product (`*`): Take the product of two potentials.\n
    2. Coercion (`coerce`): Coerce the potential to operate on another potential's vocabulary.\n
    3. Auto-batching (`to_autobatched`): Create a version that automatically batches concurrent requests to the instance methods.\n
    4. Parallelization (`to_multiprocess`): Create a version that parallelizes operations over multiple processes.\n
    """

    def __mul__(self, other):
        return self.coerce(other, lambda x, y: x * y)

    def coerce(self, other, f, prune=True):
        if isinstance(other, self.__class__):
            return f(self, other)
        else:
            raise TypeError(f"Cannot coerce {type(other)} to {self.__class__}")

    def to_autobatched(self):
        def autobatched_method(method, *args, batch_size=32, **kwargs):
            results = []
            for i in range(0, len(args[0]), batch_size):
                batch_args = [arg[i:i+batch_size] for arg in args]
                results.extend(method(*batch_args, **kwargs))
            return results

        return type(self)(
            **{name: partial(autobatched_method, getattr(self, name))
               for name in dir(self) if callable(getattr(self, name))})

    def to_multiprocess(self, num_workers=2, spawn_args=None):
        def multiprocess_method(method, *args, **kwargs):
            with ProcessPoolExecutor(max_workers=num_workers, initargs=spawn_args) as executor:
                return list(executor.map(lambda x: method(*x), zip(*args)))

        return type(self)(
            **{name: partial(multiprocess_method, getattr(self, name))
               for name in dir(self) if callable(getattr(self, name))})