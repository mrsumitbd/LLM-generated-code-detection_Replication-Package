from multiprocessing import Pool

class PotentialOps:
    """Mixin providing operations for potential functions:

    1. Product (`*`): Take the product of two potentials.\n
    2. Coercion (`coerce`): Coerce the potential to operate on another potential's vocabulary.\n
    3. Auto-batching (`to_autobatched`): Create a version that automatically batches concurrent requests to the instance methods.\n
    4. Parallelization (`to_multiprocess`): Create a version that parallelizes operations over multiple processes.\n
    """

    def __mul__(self, other):
        return self.product(other)

    def coerce(self, other, f, prune=True):
        return self.coerce_to(other, f, prune)

    def to_autobatched(self):
        return self.autobatched()

    def to_multiprocess(self, num_workers=2, spawn_args=None):
        return self.multiprocess(num_workers, spawn_args)

    def product(self, other):
        pass

    def coerce_to(self, other, f, prune=True):
        pass

    def autobatched(self):
        pass

    def multiprocess(self, num_workers=2, spawn_args=None):
        pass