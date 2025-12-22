class Ware:

    def __init__(self, name: str = "", price: float = 0.0, quantity: int = 0):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_csv(self) -> str:
        return f"{self.name},{self.price},{self.quantity}"