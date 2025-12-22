from typing import List, Tuple, Optional
from collections import Counter
from colorthief import ColorThief
from PIL import Image
import colorsys

class ImageColorExtractor:
    """图片颜色提取器"""

    def __init__(self):
        pass

    def extract_colors(self, image_path: str, num_colors: int = 5, resize_width: int = 150) -> List[Tuple[int, int, int]]:
        image = Image.open(image_path)
        if resize_width:
            image.thumbnail((resize_width, resize_width * image.height // image.width))
        color_thief = ColorThief(image_path)
        return color_thief.get_palette(color_count=num_colors)

    def get_dominant_color(self, image_path: str) -> Optional[Tuple[int, int, int]]:
        color_thief = ColorThief(image_path)
        return color_thief.get_color()

    def get_color_palette(self, image_path: str, num_colors: int = 5) -> List[str]:
        colors = self.extract_colors(image_path, num_colors)
        return [self.rgb_to_hex(color) for color in colors]

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        return '#%02x%02x%02x' % rgb

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    @staticmethod
    def is_dark_color(rgb: Tuple[int, int, int]) -> bool:
        r, g, b = rgb
        hue, lightness, _ = colorsys.rgb_to_hls(r/255, g/255, b/255)
        return lightness < 0.5

    def get_complementary_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        r, g, b = rgb
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        h = (h + 0.5) % 1
        r, g, b = [int(c*255) for c in colorsys.hls_to_rgb(h, l, s)]
        return (r, g, b)

    def get_color_info(self, image_path: str, num_colors: int = 5) -> dict:
        colors = self.extract_colors(image_path, num_colors)
        color_info = {}
        for color in colors:
            hex_color = self.rgb_to_hex(color)
            color_info[hex_color] = {
                'rgb': color,
                'is_dark': self.is_dark_color(color),
                'complementary': self.get_complementary_color(color)
            }
        return color_info