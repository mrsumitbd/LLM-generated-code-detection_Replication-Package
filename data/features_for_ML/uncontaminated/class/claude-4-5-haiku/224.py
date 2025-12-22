from typing import List, Tuple, Optional
from PIL import Image
from collections import Counter
import colorsys


class ImageColorExtractor:
    """图片颜色提取器"""

    def __init__(self):
        pass

    def extract_colors(self, image_path: str, num_colors: int = 5, resize_width: int = 150) -> List[Tuple[int, int, int]]:
        """Extract dominant colors from image"""
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image for faster processing
            aspect_ratio = image.height / image.width
            new_height = int(resize_width * aspect_ratio)
            image = image.resize((resize_width, new_height), Image.Resampling.LANCZOS)
            
            # Get all pixels
            pixels = list(image.getdata())
            
            # Count color frequencies
            color_counts = Counter(pixels)
            
            # Get most common colors
            most_common = color_counts.most_common(num_colors)
            colors = [color for color, count in most_common]
            
            return colors
        except Exception as e:
            return []

    def get_dominant_color(self, image_path: str) -> Optional[Tuple[int, int, int]]:
        """Get the most dominant color from image"""
        colors = self.extract_colors(image_path, num_colors=1)
        return colors[0] if colors else None

    def get_color_palette(self, image_path: str, num_colors: int = 5) -> List[str]:
        """Get color palette as hex strings"""
        colors = self.extract_colors(image_path, num_colors=num_colors)
        return [self.rgb_to_hex(color) for color in colors]

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex string"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """Convert hex string to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def is_dark_color(rgb: Tuple[int, int, int]) -> bool:
        """Check if color is dark"""
        # Calculate luminance using relative luminance formula
        r, g, b = [x / 255.0 for x in rgb]
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 0.5

    def get_complementary_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get complementary color"""
        # Convert RGB to HSV
        r, g, b = [x / 255.0 for x in rgb]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        
        # Shift hue by 180 degrees
        h = (h + 0.5) % 1.0
        
        # Convert back to RGB
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))

    def get_color_info(self, image_path: str, num_colors: int = 5) -> dict:
        """Get comprehensive color information"""
        colors = self.extract_colors(image_path, num_colors=num_colors)
        
        color_info = {
            'dominant_color': colors[0] if colors else None,
            'dominant_color_hex': self.rgb_to_hex(colors[0]) if colors else None,
            'palette': colors,
            'palette_hex': [self.rgb_to_hex(color) for color in colors],
            'is_dominant_dark': self.is_dark_color(colors[0]) if colors else None,
            'complementary_color': self.get_complementary_color(colors[0]) if colors else None,
            'complementary_color_hex': self.rgb_to_hex(self.get_complementary_color(colors[0])) if colors else None,
        }
        
        return color_info