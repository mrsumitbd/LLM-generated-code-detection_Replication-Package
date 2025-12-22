from __future__ import annotations

import os
from typing import List, Tuple, Optional

import numpy as np
from PIL import Image
from sklearn.cluster import KMeans


class ImageColorExtractor:
    """图片颜色提取器"""

    def __init__(self):
        pass

    def _load_and_resize(self, image_path: str, resize_width: int) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        img = Image.open(image_path).convert("RGB")
        w, h = img.size
        if w != resize_width:
            h = int(h * resize_width / w)
            img = img.resize((resize_width, h), Image.LANCZOS)
        return np.array(img)

    def extract_colors(
        self, image_path: str, num_colors: int = 5, resize_width: int = 150
    ) -> List[Tuple[int, int, int]]:
        """返回图片中最主要的 num_colors 个 RGB 颜色"""
        img = self._load_and_resize(image_path, resize_width)
        pixels = img.reshape(-1, 3).astype(np.float32)
        kmeans = KMeans(n_clusters=num_colors, random_state=0, n_init="auto")
        kmeans.fit(pixels)
        centers = kmeans.cluster_centers_.astype(int)
        # 按簇大小排序
        labels, counts = np.unique(kmeans.labels_, return_counts=True)
        sorted_idx = np.argsort(-counts)
        sorted_centers = centers[labels[sorted_idx]]
        return [tuple(c) for c in sorted_centers]

    def get_dominant_color(self, image_path: str) -> Optional[Tuple[int, int, int]]:
        """返回图片最主要的颜色"""
        try:
            return self.extract_colors(image_path, num_colors=1)[0]
        except Exception:
            return None

    def get_color_palette(
        self, image_path: str, num_colors: int = 5
    ) -> List[str]:
        """返回图片的颜色调色板（十六进制字符串）"""
        rgb_colors = self.extract_colors(image_path, num_colors)
        return [self.rgb_to_hex(c) for c in rgb_colors]

    @staticmethod
    def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
        """RGB 转十六进制"""
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    @staticmethod
    def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
        """十六进制转 RGB"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def is_dark_color(rgb: Tuple[int, int, int]) -> bool:
        """判断颜色是否偏暗（基于感知亮度）"""
        r, g, b = rgb
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        return luminance < 128

    def get_complementary_color(self, rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """返回给定颜色的互补色"""
        return tuple(255 - v for v in rgb)

    def get_color_info(
        self, image_path: str, num_colors: int = 5
    ) -> dict:
        """返回图片颜色信息的完整字典"""
        rgb_colors = self.extract_colors(image_path, num_colors)
        hex_colors = [self.rgb_to_hex(c) for c in rgb_colors]
        info = {
            "dominant_color_rgb": rgb_colors[0],
            "dominant_color_hex": hex_colors[0],
            "palette_rgb": rgb_colors,
            "palette_hex": hex_colors,
            "is_dark": [self.is_dark_color(c) for c in rgb_colors],
            "complementary_rgb": [self.get_complementary_color(c) for c in rgb_colors],
            "complementary_hex": [self.rgb_to_hex(self.get_complementary_color(c)) for c in rgb_colors],
        }
        return info