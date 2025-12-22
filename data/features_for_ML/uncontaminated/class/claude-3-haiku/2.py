class GreetingService:
    """Simple greeting service"""

    def __init__(self):
        self.greetings = ["Hello", "Hi", "Howdy", "Greetings"]

    def greet(self, name: str):
        greeting = self.greetings[len(name) % len(self.greetings)]
        return f"{greeting}, {name}!"