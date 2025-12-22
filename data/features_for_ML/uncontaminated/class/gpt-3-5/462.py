class Ware:
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_csv(self) -> str:
        return f"{self.name},{self.price},{self.quantity}"