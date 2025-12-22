class Shell:
    """Interactive CLI shell for dialog with Quantalogic agents."""

    def __init__(self, agent_config: Optional[AgentConfig] = None, cli_log_level: Optional[str] = None):
        self.agent_config = agent_config or AgentConfig()
        self.cli_log_level = cli_log_level or "INFO"
        self._agent: Optional[Agent] = None
        self._message_history: List[Dict[str, str]] = []
        self._commands: Dict[str, Callable] = {}
        self._session: Optional[PromptSession] = None
        self._running = False
        
        self._setup_logging()
        self._initialize_agent()
        self._register_builtin_commands()
        self._load_plugin_commands()

    def _setup_logging(self) -> None:
        """Configure logging for the shell."""
        logging.basicConfig(
            level=getattr(logging, self.cli_log_level.upper(), logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def _initialize_agent(self) -> None:
        """Initialize the agent from config."""
        try:
            self._agent = Agent(config=self.agent_config)
            self.logger.info("Agent initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize agent: {e}")
            self._agent = None

    @property
    def current_agent(self) -> Agent:
        """Get the current agent instance."""
        if self._agent is None:
            raise RuntimeError("Agent not initialized")
        return self._agent

    @property
    def current_message_history(self) -> List[Dict[str, str]]:
        """Get the current message history."""
        return self._message_history.copy()

    def _register_builtin_commands(self) -> None:
        """Register built-in shell commands."""
        self._commands = {
            "help": self._cmd_help,
            "clear": self._cmd_clear,
            "history": self._cmd_history,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
            "reset": self._cmd_reset,
            "config": self._cmd_config,
        }

    def _cmd_help(self, *args) -> None:
        """Display help information."""
        print("\nAvailable commands:")
        for cmd in sorted(self._commands.keys()):
            print(f"  {cmd}")
        print("\nType 'help <command>' for more information.\n")

    def _cmd_clear(self, *args) -> None:
        """Clear the screen."""
        import os
        os.system('clear' if os.name == 'posix' else 'cls')

    def _cmd_history(self, *args) -> None:
        """Display message history."""
        if not self._message_history:
            print("No message history available.")
            return
        print("\nMessage History:")
        for i, msg in enumerate(self._message_history, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:100]
            print(f"{i}. [{role}]: {content}...")
        print()

    def _cmd_exit(self, *args) -> None:
        """Exit the shell."""
        self._running = False
        print("Goodbye!")

    def _cmd_reset(self, *args) -> None:
        """Reset message history."""
        self._message_history = []
        print("Message history cleared.")

    def _cmd_config(self, *args) -> None:
        """Display current configuration."""
        print("\nCurrent Configuration:")
        print(f"  Log Level: {self.cli_log_level}")
        print(f"  Agent Config: {self.agent_config}")
        print()

    def _load_plugin_commands(self) -> None:
        """Load plugin commands from external sources."""
        try:
            plugin_dir = Path(__file__).parent / "plugins"
            if plugin_dir.exists():
                for plugin_file in plugin_dir.glob("*.py"):
                    if plugin_file.name.startswith("_"):
                        continue
                    try:
                        spec = importlib.util.spec_from_file_location(
                            plugin_file.stem, plugin_file
                        )
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, "register_commands"):
                                module.register_commands(self._commands)
                    except Exception as e:
                        self.logger.warning(f"Failed to load plugin {plugin_file.name}: {e}")
        except Exception as e:
            self.logger.debug(f"Plugin loading error: {e}")

    def bottom_toolbar(self):
        """Return the bottom toolbar content for the prompt."""
        agent_status = "✓ Agent Ready" if self._agent else "✗ Agent Error"
        history_count = len(self._message_history)
        return f" {agent_status} | Messages: {history_count} | Type 'help' for commands"

    def _process_command(self, user_input: str) -> bool:
        """Process user input as a command."""
        if not user_input.startswith("/"):
            return False
        
        parts = user_input[1:].split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else ()
        
        if cmd in self._commands:
            try:
                self._commands[cmd](*args)
            except Exception as e:
                self.logger.error(f"Command error: {e}")
            return True
        else:
            print(f"Unknown command: /{cmd}")
            return True

    async def _send_message(self, message: str) -> str:
        """Send a message to the agent and get response."""
        try:
            self._message_history.append({"role": "user", "content": message})
            response = await self.current_agent.process(message, self._message_history)
            self._message_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return f"Error: {str(e)}"

    async def run(self) -> None:
        """Run the interactive shell."""
        self._running = True
        self._session = PromptSession(
            bottom_toolbar=self.bottom_toolbar,
            completer=WordCompleter(list(self._commands.keys()), ignore_case=True),
        )
        
        print("Welcome to Quantalogic Shell")
        print("Type 'help' for available commands or 'exit' to quit.\n")
        
        while self._running:
            try:
                user_input = await self._session.prompt_async(">>> ")
                
                if not user_input.strip():
                    continue
                
                if self._process_command(user_input):
                    continue
                
                response = await self._send_message(user_input)
                print(f"\nAgent: {response}\n")
                
            except KeyboardInterrupt:
                print("\nUse '/exit' to quit.")
            except EOFError:
                break
            except Exception as e:
                self.logger.error(f"Shell error: {e}")
                print(f"Error: {e}")