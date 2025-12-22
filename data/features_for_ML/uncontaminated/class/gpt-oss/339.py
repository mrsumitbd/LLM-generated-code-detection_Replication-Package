class Client:
    def __init__(self):
        self.loaded_modules = set()
        self.speaker_enabled = False
        self.prompt = "> "
        self.running = True

    def _handle_load(self, args_list: list):
        if not args_list:
            print("Usage: load <module_name>")
            return
        module = args_list[0]
        if module in self.loaded_modules:
            print(f"Module '{module}' already loaded.")
        else:
            self.loaded_modules.add(module)
            print(f"Loaded module '{module}'.")

    def _handle_unload(self, args_list: list):
        if not args_list:
            print("Usage: unload <module_name>")
            return
        module = args_list[0]
        if module in self.loaded_modules:
            self.loaded_modules.remove(module)
            print(f"Unloaded module '{module}'.")
        else:
            print(f"Module '{module}' not loaded.")

    def _handle_speaker(self, args_list: list):
        self.speaker_enabled = not self.speaker_enabled
        state = "enabled" if self.speaker_enabled else "disabled"
        print(f"Speaker {state}.")

    def _handle_prompt(self, args_list: list):
        if args_list:
            self.prompt = args_list[0]
            print(f"Prompt set to '{self.prompt}'.")
        else:
            print(f"Current prompt: '{self.prompt}'")

    def _handle_say(self, args_list: list):
        if not args_list:
            print("Usage: say <message>")
            return
        message = " ".join(args_list)
        print(message)
        if self.speaker_enabled:
            print(f"[Speaking] {message}")

    @staticmethod
    def _handle_stop(args_list: list):
        print("Stopping client.")
        return False

    def _handle_help(self, args_list: list):
        commands = {
            "load": "Load a module. Usage: load <module_name>",
            "unload": "Unload a module. Usage: unload <module_name>",
            "speaker": "Toggle speaker on/off.",
            "prompt": "Set or show the prompt. Usage: prompt <new_prompt>",
            "say": "Print a message. Usage: say <message>",
            "stop": "Exit the client.",
            "help": "Show this help message."
        }
        for cmd, desc in commands.items():
            print(f"{cmd:<10} - {desc}")

    def run(self):
        command_map = {
            "load": self._handle_load,
            "unload": self._handle_unload,
            "speaker": self._handle_speaker,
            "prompt": self._handle_prompt,
            "say": self._handle_say,
            "stop": self._handle_stop,
            "help": self._handle_help
        }
        while self.running:
            try:
                line = input(self.prompt)
            except EOFError:
                break
            if not line.strip():
                continue
            parts = line.strip().split()
            cmd, args = parts[0], parts[1:]
            handler = command_map.get(cmd)
            if handler:
                result = handler(args)
                if result is False:
                    self.running = False
            else:
                print(f"Unknown command: {cmd}. Type 'help' for a list of commands.")