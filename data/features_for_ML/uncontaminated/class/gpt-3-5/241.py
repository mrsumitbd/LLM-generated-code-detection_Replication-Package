from typing import Callable

class DrawingAction:

    def draw(self, cr: cairo.Context, image_to_widget_coords: Callable[[int, int], tuple[float, float]], scale: float):
        pass

    def get_bounds(self) -> QuadBounds:
        pass

    def contains_point(self, x_img: int, y_img: int) -> bool:
        pass

    def _calculate_shadow_color(self, color):
        pass

    def translate(self, dx: int, dy: int):
        pass

    def get_drawing_mode(self) -> DrawingMode:
        pass