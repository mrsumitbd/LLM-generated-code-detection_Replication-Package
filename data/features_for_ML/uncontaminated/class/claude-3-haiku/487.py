class Floor:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def area(self):
        return self.x * self.y

    def perimeter(self):
        return 2 * (self.x + self.y)

    def __str__(self):
        return f"Floor with dimensions {self.x} x {self.y}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y