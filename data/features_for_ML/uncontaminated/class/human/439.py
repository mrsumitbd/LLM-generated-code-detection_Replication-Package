from typing import Optional, List, Tuple

class DisplayConfig:
    """Complete display configuration"""
    # Background (required)
    background_path: str
    background_type: BackgroundType

    # Output dimensions
    output_width: int = 320
    output_height: int = 240

    # Display rotation (0, 90, 180, 270 degrees)
    rotation: int = 0

    # Global font configuration (applies to all text elements)
    global_font_path: Optional[str] = None

    # Foreground image (optional)
    foreground_image_path: Optional[str] = None
    foreground_position: Tuple[int, int] = (0, 0)
    foreground_alpha: float = 1.0  # 0.0 = transparent, 1.0 = opaque

    # Metrics configuration
    metrics_configs: List[MetricConfig] = None

    # Date configuration
    date_config: Optional[TextConfig] = None

    # Time configuration
    time_config: Optional[TextConfig] = None

    def __post_init__(self):
        if self.metrics_configs is None:
            self.metrics_configs = []