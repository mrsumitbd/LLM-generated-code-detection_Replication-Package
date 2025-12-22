class Client:

    def __init__(self):
        self.running = True

    def _handle_load(self, args_list: list):
        print(f"Loading: {args_list}")

    def _handle_unload(self, args_list: list):
        print(f"Unloading: {args_list}")

    def _handle_speaker(self, args_list: list):
        print(f"Speaker: {args_list}")

    def _handle_prompt(self, args_list: list):
        print(f"Prompt: {args_list}")

    def _handle_say(self, args_list: list):
        print(f"Saying: {args_list}")

    @staticmethod
    def _handle_stop(args_list: list):
        print(f"Stopping: {args_list}")
        exit()

    def _handle_help(self, args_list: list):
        print("Help command executed.")

    def run(self):
        while self.running:
            command = input("Enter a command: ")
            command_parts = command.split()
            if command_parts:
                command_name = command_parts[0]
                args_list = command_parts[1:]
                if hasattr(self, f"_handle_{command_name}"):
                    getattr(self, f"_handle_{command_name}")(args_list)
                else:
                    print("Invalid command. Type 'help' for available commands.")