class DrawingAction:
    def __init__(self, x: int = 0, y: int = 0, color: tuple = (0, 0, 0), drawing_mode: DrawingMode = DrawingMode.PEN):
        self.x = x
        self.y = y
        self.color = color
        self.drawing_mode = drawing_mode
        self.points = []
        self.bounds = QuadBounds(x, y, x, y)

    def draw(self, cr: cairo.Context, image_to_widget_coords: Callable[[int, int], tuple[float, float]], scale: float):
        if not self.points:
            return
        
        widget_points = [image_to_widget_coords(int(p[0]), int(p[1])) for p in self.points]
        
        cr.set_source_rgb(*self.color)
        cr.set_line_width(2.0 * scale)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        
        if widget_points:
            cr.move_to(widget_points[0][0], widget_points[0][1])
            for point in widget_points[1:]:
                cr.line_to(point[0], point[1])
            cr.stroke()

    def get_bounds(self) -> QuadBounds:
        if not self.points:
            return QuadBounds(self.x, self.y, self.x, self.y)
        
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        
        min_x = min(xs)
        max_x = max(xs)
        min_y = min(ys)
        max_y = max(ys)
        
        return QuadBounds(int(min_x), int(min_y), int(max_x), int(max_y))

    def contains_point(self, x_img: int, y_img: int) -> bool:
        if not self.points or len(self.points) < 2:
            return False
        
        threshold = 5
        
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            
            distance = self._point_to_line_distance(x_img, y_img, x1, y1, x2, y2)
            if distance <= threshold:
                return True
        
        return False

    def _point_to_line_distance(self, px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5

    def _calculate_shadow_color(self, color):
        r, g, b = color
        shadow_factor = 0.5
        return (r * shadow_factor, g * shadow_factor, b * shadow_factor)

    def translate(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
        self.points = [(p[0] + dx, p[1] + dy) for p in self.points]
        bounds = self.get_bounds()
        self.bounds = bounds

    def get_drawing_mode(self) -> DrawingMode:
        return self.drawing_mode

    def add_point(self, x: int, y: int):
        self.points.append((x, y))
        bounds = self.get_bounds()
        self.bounds = bounds