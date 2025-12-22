import sys
from typing import Any, Dict, Optional

class InteractiveMode:
    """Handles interactive mode operations."""

    def __init__(self):
        self.agent: Optional[SparkStrandsAgent] = None

    async def run(self) -> None:
        """Run interactive mode."""
        try:
            model = self._get_model_choice()
            self.agent = SparkStrandsAgent(model=model, verbose=True)

            if not await self.agent.initialize():
                console_print("❌ Failed to initialize agent")
                return

            await self._interaction_loop(model)
        finally:
            if self.agent:
                self.agent.close()
            console_print("\n👋 \033[1mGoodbye!\033[0m")

    def _get_model_choice(self) -> str:
        """Get user's model choice."""
        console_print("🎯 \033[1mModel Options:\033[0m")
        for model, info in Config.MODEL_OPTIONS.items():
            style = "\033[93m" if "1.7b" in model else "\033[92m"
            rec = " \033[1m[RECOMMENDED]\033[0m" if "1.7b" in model else ""
            console_print(
                f"  - {style}{model}\033[0m ({info['quality'].lower()}, {info['speed'].lower()}, {info['size']}){rec}"
            )

        # Check if running in interactive mode
        if not sys.stdin.isatty():
            console_print(
                f"\n🤖 Non-interactive mode: Using default model [{Config.DEFAULT_MODEL}]"
            )
            return Config.DEFAULT_MODEL

        try:
            return (
                input(f"\n🤖 Choose model [{Config.DEFAULT_MODEL}]: ").strip()
                or Config.DEFAULT_MODEL
            )
        except EOFError:
            console_print(
                f"\n🤖 EOF detected: Using default model [{Config.DEFAULT_MODEL}]"
            )
            return Config.DEFAULT_MODEL

    async def _interaction_loop(self, model: str) -> None:
        """Main interaction loop."""
        self._print_ready_message(model)

        while True:
            try:
                # Check if running in interactive mode
                if not sys.stdin.isatty():
                    console_print("\n❌ Non-interactive environment detected. Exiting.")
                    break

                user_input = input("\n💬 \033[1mYour query:\033[0m ").strip()

                if user_input.lower() in ["exit", "quit", "bye"]:
                    break
                elif user_input.lower() == "help":
                    self._print_help()
                    continue
                elif not user_input:
                    continue

                console_print("\n🔄 Processing query with Strands Agent...")
                response = await self.agent.query(user_input)
                console_print(response)
                console_print("\n" + "\033[90m" + "─" * 80 + "\033[0m")

            except KeyboardInterrupt:
                break
            except EOFError:
                console_print("\n❌ EOF detected. Exiting interactive mode.")
                break
            except Exception as e:
                console_print(f"\n❌ Error: {e}")

    def _print_ready_message(self, model: str) -> None:
        """Print ready message with examples."""
        console_print(
            f"\n🎉 \033[1mStrands Spark Analysis Agent Ready!\033[0m (Using {model})"
        )
        console_print("\n📝 \033[1mExample commands:\033[0m")
        console_print(f"  - Get detailed analysis for {Config.SAMPLE_APPS[0]}")
        console_print(f"  - Analyze performance bottlenecks in {Config.SAMPLE_APPS[1]}")
        console_print("  - help | exit")
        console_print("\n📊 \033[1mAvailable sample app IDs:\033[0m")
        for app in Config.SAMPLE_APPS:
            console_print(f"  - \033[90m{app}\033[0m")

    def _print_help(self) -> None:
        """Print help information."""
        console_print("\n🔧 \033[1mCommands:\033[0m")
        console_print("  - Any natural language query about Spark applications")
        console_print("  - Use the sample app IDs provided above")
        console_print("  - \033[1mexit\033[0m: Quit the program")
        console_print("\n💡 \033[1mExample queries:\033[0m")
        console_print("  - 'What are the slowest stages in [app-id]?'")
        console_print("  - 'Analyze memory usage for [app-id]'")
        console_print("  - 'Compare performance between applications'")