class InteractiveMode:
    """Handles interactive mode operations."""

    def __init__(self):
        pass

    def _get_model_choice(self) -> str:
        choice = input("Enter the model choice: ")
        return choice

    def _print_ready_message(self, model: str) -> None:
        print(f"Model {model} is ready for use.")

    def _print_help(self) -> None:
        print("Help: This is the interactive mode. You can choose a model and use it.")