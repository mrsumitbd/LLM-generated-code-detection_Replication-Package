class Client:

    def __init__(self):
        self.tts_engine = None
        self.current_speaker = None
        self.current_prompt = ""
        self.commands = {
            'load': self._handle_load,
            'unload': self._handle_unload,
            'speaker': self._handle_speaker,
            'prompt': self._handle_prompt,
            'say': self._handle_say,
            'stop': self._handle_stop,
            'help': self._handle_help
        }

    def _handle_load(self, args_list: list):
        if not args_list:
            print("Error: load requires an engine name")
            return
        engine_name = args_list[0]
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init(engine_name)
            print(f"Loaded TTS engine: {engine_name}")
        except Exception as e:
            print(f"Error loading engine: {e}")

    def _handle_unload(self, args_list: list):
        if self.tts_engine:
            try:
                self.tts_engine = None
                print("TTS engine unloaded")
            except Exception as e:
                print(f"Error unloading engine: {e}")
        else:
            print("No engine loaded")

    def _handle_speaker(self, args_list: list):
        if not self.tts_engine:
            print("Error: No TTS engine loaded")
            return
        if not args_list:
            print("Error: speaker requires a speaker ID")
            return
        try:
            speaker_id = int(args_list[0])
            voices = self.tts_engine.getProperty('voices')
            if 0 <= speaker_id < len(voices):
                self.tts_engine.setProperty('voice', voices[speaker_id].id)
                self.current_speaker = speaker_id
                print(f"Speaker set to: {speaker_id}")
            else:
                print(f"Error: Speaker ID {speaker_id} out of range")
        except ValueError:
            print("Error: Speaker ID must be an integer")
        except Exception as e:
            print(f"Error setting speaker: {e}")

    def _handle_prompt(self, args_list: list):
        if not args_list:
            print("Error: prompt requires text")
            return
        self.current_prompt = " ".join(args_list)
        print(f"Prompt set to: {self.current_prompt}")

    def _handle_say(self, args_list: list):
        if not self.tts_engine:
            print("Error: No TTS engine loaded")
            return
        text = " ".join(args_list) if args_list else self.current_prompt
        if not text:
            print("Error: No text to say")
            return
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error saying text: {e}")

    @staticmethod
    def _handle_stop(args_list: list):
        print("Stop command executed")

    def _handle_help(self, args_list: list):
        help_text = """
Available commands:
  load <engine>       - Load a TTS engine (e.g., sapi5, espeak)
  unload              - Unload the current TTS engine
  speaker <id>        - Set the speaker/voice (0, 1, 2, ...)
  prompt <text>       - Set the default prompt text
  say [text]          - Speak the text (or use current prompt if no text given)
  stop                - Stop speaking
  help                - Show this help message
  exit                - Exit the program
        """
        print(help_text)

    def run(self):
        print("TTS Client started. Type 'help' for commands.")
        while True:
            try:
                user_input = input("> ").strip()
                if not user_input:
                    continue
                
                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1].split() if len(parts) > 1 else []
                
                if command == 'exit':
                    print("Exiting...")
                    break
                
                if command in self.commands:
                    self.commands[command](args)
                else:
                    print(f"Unknown command: {command}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")