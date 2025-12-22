class DisplayConfig:
    """Complete display configuration"""

    def __init__(self, resolution, refresh_rate, color_depth, aspect_ratio):
        self.resolution = resolution
        self.refresh_rate = refresh_rate
        self.color_depth = color_depth
        self.aspect_ratio = aspect_ratio

    def __post_init__(self):
        self._validate_resolution()
        self._validate_refresh_rate()
        self._validate_color_depth()
        self._validate_aspect_ratio()

    def _validate_resolution(self):
        width, height = self.resolution.split('x')
        if not width.isdigit() or not height.isdigit():
            raise ValueError("Invalid resolution format. Expected 'WIDTHxHEIGHT'.")
        if int(width) <= 0 or int(height) <= 0:
            raise ValueError("Resolution values must be positive integers.")

    def _validate_refresh_rate(self):
        if not isinstance(self.refresh_rate, (int, float)) or self.refresh_rate <= 0:
            raise ValueError("Refresh rate must be a positive number.")

    def _validate_color_depth(self):
        if not isinstance(self.color_depth, int) or self.color_depth <= 0:
            raise ValueError("Color depth must be a positive integer.")

    def _validate_aspect_ratio(self):
        width, height = self.aspect_ratio.split(':')
        if not width.isdigit() or not height.isdigit():
            raise ValueError("Invalid aspect ratio format. Expected 'WIDTH:HEIGHT'.")
        if int(width) <= 0 or int(height) <= 0:
            raise ValueError("Aspect ratio values must be positive integers.")