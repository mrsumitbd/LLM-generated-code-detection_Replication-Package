class InteractiveMode:
    """Handles interactive mode operations."""

    def __init__(self):
        self.model_choices = ["model1", "model2", "model3"]

    def _get_model_choice(self) -> str:
        while True:
            print("Available models:")
            for model in self.model_choices:
                print(f"- {model}")
            user_input = input("Enter the model name or 'help' for more information: ")
            if user_input.lower() == "help":
                self._print_help()
            elif user_input in self.model_choices:
                return user_input
            else:
                print("Invalid model choice. Please try again.")

    def _print_ready_message(self, model: str) -> None:
        print(f"You have selected the '{model}' model. The system is ready for use.")

    def _print_help(self) -> None:
        print("Interactive mode allows you to select a model and use it.")
        print("To select a model, enter the model name from the list of available models.")
        print("Type 'help' at any time to display this information.")