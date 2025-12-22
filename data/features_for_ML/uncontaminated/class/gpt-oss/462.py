class Ware:
    def __init__(self, id: int, name: str, price: float, quantity: int):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_csv(self) -> str:
        header = "id,name,price,quantity"
        values = f"{self.id},{self.name},{self.price},{self.quantity}"
        return f"{header}\n{values}"