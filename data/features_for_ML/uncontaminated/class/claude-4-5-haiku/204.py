class TqdmPositionRegistry:
    """
    A simple registry for tqdm positions.
    """
    
    _positions = set()
    _lock = __import__('threading').Lock()

    @classmethod
    def claim(cls) -> int:
        with cls._lock:
            pos = 0
            while pos in cls._positions:
                pos += 1
            cls._positions.add(pos)
            return pos

    @classmethod
    def release(cls, pos: int):
        with cls._lock:
            cls._positions.discard(pos)