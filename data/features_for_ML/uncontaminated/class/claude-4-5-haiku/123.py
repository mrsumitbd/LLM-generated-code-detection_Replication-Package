class PotentialOps:
    """Mixin providing operations for potential functions:

    1. Product (`*`): Take the product of two potentials.\n
    2. Coercion (`coerce`): Coerce the potential to operate on another potential's vocabulary.\n
    3. Auto-batching (`to_autobatched`): Create a version that automatically batches concurrent requests to the instance methods.\n
    4. Parallelization (`to_multiprocess`): Create a version that parallelizes operations over multiple processes.\n
    """

    def __mul__(self, other):
        """Take the product of two potentials."""
        from functools import wraps
        
        if not isinstance(other, PotentialOps):
            return NotImplemented
        
        self_call = self.__call__
        other_call = other.__call__
        
        @wraps(self_call)
        def product_call(x):
            return self_call(x) * other_call(x)
        
        result = type(self).__new__(type(self))
        result.__call__ = product_call
        return result

    def coerce(self, other, f, prune=True):
        """Coerce the potential to operate on another potential's vocabulary."""
        from functools import wraps
        
        self_call = self.__call__
        
        @wraps(self_call)
        def coerced_call(x):
            return self_call(f(x))
        
        result = type(self).__new__(type(self))
        result.__call__ = coerced_call
        return result

    def to_autobatched(self):
        """Create a version that automatically batches concurrent requests to the instance methods."""
        from functools import wraps
        from queue import Queue
        from threading import Thread, Event
        import time
        
        self_call = self.__call__
        request_queue = Queue()
        result_dict = {}
        stop_event = Event()
        
        def batch_worker():
            while not stop_event.is_set():
                batch = []
                batch_ids = []
                
                try:
                    while len(batch) < 32:
                        request_id, x = request_queue.get(timeout=0.01)
                        batch.append(x)
                        batch_ids.append(request_id)
                except:
                    pass
                
                if batch:
                    try:
                        results = [self_call(item) for item in batch]
                        for req_id, result in zip(batch_ids, results):
                            result_dict[req_id] = result
                    except:
                        for req_id in batch_ids:
                            result_dict[req_id] = None
        
        worker_thread = Thread(target=batch_worker, daemon=True)
        worker_thread.start()
        
        request_counter = [0]
        
        @wraps(self_call)
        def autobatched_call(x):
            request_id = request_counter[0]
            request_counter[0] += 1
            request_queue.put((request_id, x))
            
            while request_id not in result_dict:
                time.sleep(0.001)
            
            result = result_dict.pop(request_id)
            return result
        
        result = type(self).__new__(type(self))
        result.__call__ = autobatched_call
        result._worker_thread = worker_thread
        result._stop_event = stop_event
        return result

    def to_multiprocess(self, num_workers=2, spawn_args=None):
        """Create a version that parallelizes operations over multiple processes."""
        from functools import wraps
        from multiprocessing import Pool, Manager
        from queue import Queue
        import threading
        
        self_call = self.__call__
        
        pool = Pool(processes=num_workers)
        
        @wraps(self_call)
        def multiprocess_call(x):
            result = pool.apply(self_call, (x,))
            return result
        
        result = type(self).__new__(type(self))
        result.__call__ = multiprocess_call
        result._pool = pool
        return result