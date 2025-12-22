class Client:
    def __init__(self):
        self.current_speaker = None
        self.prompt = ">>> "
        self.running = True

    def _handle_load(self, args_list: list):
        if len(args_list) < 1:
            print("Usage: load <filename>")
            return
        filename = args_list[0]
        # Load the file and set the current speaker
        self.current_speaker = load_speaker(filename)
        print(f"Loaded speaker: {self.current_speaker.name}")

    def _handle_unload(self, args_list: list):
        if self.current_speaker is None:
            print("No speaker loaded.")
            return
        self.current_speaker = None
        print("Speaker unloaded.")

    def _handle_speaker(self, args_list: list):
        if self.current_speaker is None:
            print("No speaker loaded.")
            return
        print(self.current_speaker)

    def _handle_prompt(self, args_list: list):
        if len(args_list) < 1:
            print("Usage: prompt <new_prompt>")
            return
        self.prompt = args_list[0] + " "
        print(f"Prompt set to: {self.prompt}")

    def _handle_say(self, args_list: list):
        if self.current_speaker is None:
            print("No speaker loaded.")
            return
        text = " ".join(args_list)
        self.current_speaker.say(text)

    @staticmethod
    def _handle_stop(args_list: list):
        print("Stopping the client.")

    def _handle_help(self, args_list: list):
        print("Available commands:")
        print("load <filename>: Load a speaker from a file.")
        print("unload: Unload the current speaker.")
        print("speaker: Display information about the current speaker.")
        print("prompt <new_prompt>: Set a new prompt.")
        print("say <text>: Make the current speaker say the provided text.")
        print("stop: Stop the client.")
        print("help: Display this help message.")

    def run(self):
        while self.running:
            user_input = input(self.prompt).strip()
            if not user_input:
                continue
            command, *args = user_input.split()
            try:
                handler = getattr(self, f"_handle_{command}")
                handler(args)
            except AttributeError:
                print(f"Unknown command: {command}")
            except Exception as e:
                print(f"Error: {e}")
        print("Client stopped.")