import cairo
from typing import Callable
from dataclasses import dataclass

@dataclass
class QuadBounds:
    x1: float
    y1: float
    x2: float
    y2: float

class DrawingMode:
    NORMAL = 0
    SHADOW = 1

class DrawingAction:
    def __init__(self, color: tuple[float, float, float, float], drawing_mode: DrawingMode = DrawingMode.NORMAL):
        self.color = color
        self.drawing_mode = drawing_mode
        self.x = 0
        self.y = 0

    def draw(self, cr: cairo.Context, image_to_widget_coords: Callable[[int, int], tuple[float, float]], scale: float):
        cr.save()
        cr.translate(self.x, self.y)
        cr.scale(scale, scale)

        if self.drawing_mode == DrawingMode.SHADOW:
            shadow_color = self._calculate_shadow_color(self.color)
            cr.set_source_rgba(*shadow_color)
            self._draw_internal(cr, image_to_widget_coords)
            cr.restore()

        cr.set_source_rgba(*self.color)
        self._draw_internal(cr, image_to_widget_coords)
        cr.restore()

    def _draw_internal(self, cr: cairo.Context, image_to_widget_coords: Callable[[int, int], tuple[float, float]]):
        raise NotImplementedError

    def get_bounds(self) -> QuadBounds:
        raise NotImplementedError

    def contains_point(self, x_img: int, y_img: int) -> bool:
        bounds = self.get_bounds()
        x, y = image_to_widget_coords(x_img, y_img)
        return bounds.x1 <= x <= bounds.x2 and bounds.y1 <= y <= bounds.y2

    def _calculate_shadow_color(self, color):
        r, g, b, a = color
        return r * 0.5, g * 0.5, b * 0.5, a * 0.5

    def translate(self, dx: int, dy: int):
        self.x += dx
        self.y += dy

    def get_drawing_mode(self) -> DrawingMode:
        return self.drawing_mode