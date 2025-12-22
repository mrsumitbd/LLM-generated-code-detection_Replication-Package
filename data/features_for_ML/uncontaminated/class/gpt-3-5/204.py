class TqdmPositionRegistry:
    """
    A simple registry for tqdm positions.
    """
    
    _claimed_positions = set()

    @classmethod
    def claim(cls) -> int:
        pos = 0
        while pos in cls._claimed_positions:
            pos += 1
        cls._claimed_positions.add(pos)
        return pos

    @classmethod
    def release(cls, pos: int):
        cls._claimed_positions.discard(pos)