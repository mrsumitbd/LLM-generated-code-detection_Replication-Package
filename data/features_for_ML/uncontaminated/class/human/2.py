
class GreetingService:
    """Simple greeting service"""

    def __init__(self):
        print("👋 Greeting service initialized")

    def greet(self, name: str):
        return f"Hello {name} from Catzilla DI! 🚀"