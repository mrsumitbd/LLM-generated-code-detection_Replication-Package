class OtherArch:
    def __init__(self, name: str) -> None:
        self.name = name

    @override
    def __str__(self) -> str:
        return f"OtherArch(name='{self.name}')"