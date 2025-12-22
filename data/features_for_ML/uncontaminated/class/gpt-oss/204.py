import threading

class TqdmPositionRegistry:
    """
    A simple registry for tqdm positions.
    """
    _used_positions: set[int] = set()
    _lock = threading.Lock()

    @classmethod
    def claim(cls) -> int:
        """
        Claim the next available tqdm position.

        Returns:
            int: The claimed position index.
        """
        with cls._lock:
            pos = 0
            while pos in cls._used_positions:
                pos += 1
            cls._used_positions.add(pos)
            return pos

    @classmethod
    def release(cls, pos: int):
        """
        Release a previously claimed tqdm position.

        Args:
            pos (int): The position index to release.
        """
        with cls._lock:
            cls._used_positions.discard(pos)