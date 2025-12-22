class Ware:
    def __init__(self, name: str, price: float, quantity: int):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_csv(self) -> str:
        return f"{self.name},{self.price:.2f},{self.quantity}"