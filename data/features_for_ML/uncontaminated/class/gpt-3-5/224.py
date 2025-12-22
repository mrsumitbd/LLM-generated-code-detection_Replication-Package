from typing import List, Tuple, Optional

class ImageColorExtractor:
    """图片颜色提取器"""

    def __init__(self):
        pass

    def extract_colors(self, image_path: str, num_colors: int = 5, resize_width: int = 150) -> List[Tuple[int, int, int]]:
        pass

    def get_dominant_color(self, image_path: str) -> Optional[Tuple[int, int, int]]:
        pass

    def get_color_palette(self, image_path: str, num_colors: int = 5) -> List[str]:
        pass

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        pass

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        pass

    @staticmethod
    def is_dark_color(rgb: Tuple[int, int, int]) -> bool:
        pass

    def get_complementary_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        pass

    def get_color_info(self, image_path: str, num_colors: int = 5) -> dict:
        pass