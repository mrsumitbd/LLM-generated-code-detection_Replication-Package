from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class DisplayConfig:
    """Complete display configuration"""
    
    width: int = 1920
    height: int = 1080
    refresh_rate: int = 60
    fullscreen: bool = False
    vsync: bool = True
    brightness: float = 1.0
    contrast: float = 1.0
    gamma: float = 1.0
    color_depth: int = 32
    resolution_scale: float = 1.0
    antialiasing: str = "fxaa"
    texture_quality: str = "high"
    shadow_quality: str = "high"
    effects_quality: str = "high"
    render_distance: int = 100
    fov: float = 90.0
    monitor_index: int = 0
    custom_settings: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not (0.1 <= self.brightness <= 2.0):
            self.brightness = max(0.1, min(2.0, self.brightness))
        
        if not (0.1 <= self.contrast <= 2.0):
            self.contrast = max(0.1, min(2.0, self.contrast))
        
        if not (0.5 <= self.gamma <= 2.0):
            self.gamma = max(0.5, min(2.0, self.gamma))
        
        if self.width < 640:
            self.width = 640
        if self.height < 480:
            self.height = 480
        
        if self.refresh_rate < 30:
            self.refresh_rate = 30
        
        if not (0.25 <= self.resolution_scale <= 2.0):
            self.resolution_scale = max(0.25, min(2.0, self.resolution_scale))
        
        if not (30 <= self.fov <= 120):
            self.fov = max(30, min(120, self.fov))
        
        if self.render_distance < 10:
            self.render_distance = 10
        
        valid_qualities = {"low", "medium", "high", "ultra"}
        if self.antialiasing not in {"none", "fxaa", "msaa2x", "msaa4x", "msaa8x"}:
            self.antialiasing = "fxaa"
        if self.texture_quality not in valid_qualities:
            self.texture_quality = "high"
        if self.shadow_quality not in valid_qualities:
            self.shadow_quality = "high"
        if self.effects_quality not in valid_qualities:
            self.effects_quality = "high"