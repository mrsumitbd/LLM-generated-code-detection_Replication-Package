class InteractiveMode:
    """Handles interactive mode operations."""

    def __init__(self):
        # Default list of models; can be extended or overridden by subclasses
        self.available_models = ["gpt-3.5-turbo", "gpt-4"]
        self.selected_model = None

    def _get_model_choice(self) -> str:
        """
        Prompt the user to choose a model from the available list.
        Returns the chosen model string.
        """
        print("Available models:")
        for idx, model in enumerate(self.available_models, start=1):
            print(f"  {idx}. {model}")
        print("  h. Help")
        print("  q. Quit")

        while True:
            choice = input("Select a model by number (or 'h' for help, 'q' to quit): ").strip().lower()
            if choice == "q":
                print("Exiting interactive mode.")
                exit(0)
            if choice == "h":
                self._print_help()
                continue
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.available_models):
                    self.selected_model = self.available_models[idx]
                    return self.selected_model
            print("Invalid choice. Please try again or type 'h' for help.")

    def _print_ready_message(self, model: str) -> None:
        """
        Print a ready message indicating the selected model.
        """
        print(f"\n✅  Ready to use model: {model}\n")

    def _print_help(self) -> None:
        """
        Print help information for the interactive mode.
        """
        help_text = """
Interactive Mode Help
---------------------
- Enter the number corresponding to the model you wish to use.
- Type 'h' to display this help message again.
- Type 'q' to quit the interactive session.

Example:
  1   -> selects gpt-3.5-turbo
  2   -> selects gpt-4
"""
        print(help_text)