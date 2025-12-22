from dataclasses import dataclass, field

@dataclass
class DisplayConfig:
    """Complete display configuration"""

    width: int = 800
    height: int = 600
    fullscreen: bool = False
    vsync: bool = True
    title: str = "Display"
    pixel_count: int = field(init=False)

    def __post_init__(self):
        if not isinstance(self.width, int) or self.width <= 0:
            raise ValueError("width must be a positive integer")
        if not isinstance(self.height, int) or self.height <= 0:
            raise ValueError("height must be a positive integer")
        if not isinstance(self.fullscreen, bool):
            raise ValueError("fullscreen must be a boolean")
        if not isinstance(self.vsync, bool):
            raise ValueError("vsync must be a boolean")
        if not isinstance(self.title, str):
            raise ValueError("title must be a string")
        self.pixel_count = self.width * self.height

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen

    def aspect_ratio(self) -> float:
        return self.width / self.height

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(width={self.width}, height={self.height}, "
            f"fullscreen={self.fullscreen}, vsync={self.vsync}, title='{self.title}', "
            f"pixel_count={self.pixel_count})"
        )