class DisplayConfig:
    """Complete display configuration"""

    def __init__(self, resolution, refresh_rate, brightness):
        self.resolution = resolution
        self.refresh_rate = refresh_rate
        self.brightness = brightness

    def __post_init__(self):
        pass

# Example usage
display = DisplayConfig(resolution='1920x1080', refresh_rate=60, brightness=80)