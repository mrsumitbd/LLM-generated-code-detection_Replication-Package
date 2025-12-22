class GreetingService:
    """Simple greeting service"""

    def __init__(self):
        self.greeting = "Hello"

    def greet(self, name: str):
        return f"{self.greeting}, {name}!"