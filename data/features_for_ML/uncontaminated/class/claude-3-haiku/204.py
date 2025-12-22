class TqdmPositionRegistry:
    """
    A simple registry for tqdm positions.
    """

    _positions = set()

    @classmethod
    def claim(cls) -> int:
        pos = 0
        while pos in cls._positions:
            pos += 1
        cls._positions.add(pos)
        return pos

    @classmethod
    def release(cls, pos: int):
        if pos in cls._positions:
            cls._positions.remove(pos)