class RottenOrangesConfig:
    """Configuration for Rotten Oranges dataset generation"""

    def __init__(
        self,
        width: int = 10,
        height: int = 10,
        rotten_ratio: float = 0.2,
        seed: int | None = None,
    ):
        self.width = width
        self.height = height
        self.rotten_ratio = rotten_ratio
        self.seed = seed
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.width, int) or self.width <= 0:
            raise ValueError("width must be a positive integer")
        if not isinstance(self.height, int) or self.height <= 0:
            raise ValueError("height must be a positive integer")
        if not isinstance(self.rotten_ratio, (float, int)):
            raise ValueError("rotten_ratio must be a float or int")
        if not 0 <= self.rotten_ratio <= 1:
            raise ValueError("rotten_ratio must be between 0 and 1")
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("seed must be an integer or None")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(width={self.width}, "
            f"height={self.height}, rotten_ratio={self.rotten_ratio}, "
            f"seed={self.seed})"
        )