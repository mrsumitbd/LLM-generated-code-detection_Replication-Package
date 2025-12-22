
class TqdmPositionRegistry:
    """
    A simple registry for tqdm positions.
    """
    _positions = set()
    _max_positions = 100

    @classmethod
    def claim(cls) -> int:
        """
        Claim a tqdm position in the range of 0-99.
        """
        for i in range(cls._max_positions):
            if i not in cls._positions:
                cls._positions.add(i)
                return i
        raise RuntimeError("No available tqdm positions.")

    @classmethod
    def release(cls, pos: int):
        """
        Release a tqdm position.
        """
        cls._positions.discard(pos)