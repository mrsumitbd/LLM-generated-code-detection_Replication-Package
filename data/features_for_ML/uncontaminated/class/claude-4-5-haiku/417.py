import anthropic


class InteractiveMode:
    """Handles interactive mode operations."""

    def __init__(self):
        self.client = anthropic.Anthropic()
        self.conversation_history = []
        self.model = "claude-3-5-sonnet-20241022"

    def _get_model_choice(self) -> str:
        """Get model choice from user."""
        print("\nAvailable models:")
        print("1. claude-3-5-sonnet-20241022 (default)")
        print("2. claude-3-opus-20250729")
        print("3. claude-3-haiku-20250307")
        
        choice = input("\nSelect model (1-3, default 1): ").strip()
        
        models = {
            "1": "claude-3-5-sonnet-20241022",
            "2": "claude-3-opus-20250729",
            "3": "claude-3-haiku-20250307",
        }
        
        return models.get(choice, "claude-3-5-sonnet-20241022")

    def _print_ready_message(self, model: str) -> None:
        """Print ready message with model info."""
        print(f"\n✓ Ready to chat with {model}")
        print("Type 'help' for commands, 'exit' to quit\n")

    def _print_help(self) -> None:
        """Print help message."""
        print("\nAvailable commands:")
        print("  help     - Show this help message")
        print("  clear    - Clear conversation history")
        print("  model    - Change model")
        print("  exit     - Exit interactive mode")
        print("\nOr just type your message to chat!\n")

    def run(self) -> None:
        """Run interactive mode."""
        self.model = self._get_model_choice()
        self._print_ready_message(self.model)
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == "exit":
                    print("Goodbye!")
                    break
                elif user_input.lower() == "help":
                    self._print_help()
                elif user_input.lower() == "clear":
                    self.conversation_history = []
                    print("Conversation history cleared.\n")
                elif user_input.lower() == "model":
                    self.model = self._get_model_choice()
                    self._print_ready_message(self.model)
                else:
                    self._chat(user_input)
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break

    def _chat(self, user_message: str) -> None:
        """Send message and get response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        print(f"\nAssistant: {assistant_message}\n")