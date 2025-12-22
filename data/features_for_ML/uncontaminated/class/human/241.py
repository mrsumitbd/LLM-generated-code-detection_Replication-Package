import cairo
from typing import Callable
import math

class DrawingAction:
    def draw(self, cr: cairo.Context, image_to_widget_coords: Callable[[int, int], tuple[float, float]], scale: float):
        raise NotImplementedError

    def get_bounds(self) -> QuadBounds:
        raise NotImplementedError

    def contains_point(self, x_img: int, y_img: int) -> bool:
        min_x, min_y, max_x, max_y = self.get_bounds().get_bounding_rect()
        if isinstance(self, (LineAction, ArrowAction)):
            px, py = x_img, y_img
            x1, y1 = self.start
            x2, y2 = self.end
            line_len_sq = (x2 - x1) ** 2 + (y2 - y1) ** 2
            if line_len_sq == 0:
                return math.hypot(px - x1, py - y1) < (5 + self.options.size * 1.75)
            t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / line_len_sq
            t = max(0, min(1, t))
            closest_x = x1 + t * (x2 - x1)
            closest_y = y1 + t * (y2 - y1)
            dist_sq = (px - closest_x)**2 + (py - closest_y)**2
            return dist_sq < (5 + self.options.size * 1.75)**2
        return min_x <= x_img <= max_x and min_y <= y_img <= max_y

    def _calculate_shadow_color(self, color):
        r = color.red
        g = color.green
        b = color.blue
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        if luminance < 0.5:
            return (1.0, 1.0, 1.0, 0.05)
        else:
            return (0.0, 0.0, 0.0, 0.3)

    def translate(self, dx: int, dy: int):
        raise NotImplementedError

    def get_drawing_mode(self) -> DrawingMode:
        return self.options.mode