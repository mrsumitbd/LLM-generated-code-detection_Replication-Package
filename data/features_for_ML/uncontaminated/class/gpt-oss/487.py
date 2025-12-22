class Floor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Floor(x={self.x}, y={self.y})"

    def __eq__(self, other):
        if isinstance(other, Floor):
            return self.x == other.x and self.y == other.y
        return False

    def distance_to(self, other):
        if not isinstance(other, Floor):
            raise TypeError("distance_to expects a Floor instance")
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def move(self, dx, dy):
        self.x += dx
        self.y += dy