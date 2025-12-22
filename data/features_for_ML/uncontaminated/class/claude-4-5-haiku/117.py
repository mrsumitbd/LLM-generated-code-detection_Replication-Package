import anthropic
import sys
from typing import Optional


class SpinnerInterface:

    def spin(self) -> None:
        pass

    def finish(self, final_status: str) -> None:
        pass


class Spinner(SpinnerInterface):
    def __init__(self):
        self.frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.current_frame = 0
        self.is_spinning = False

    def spin(self) -> None:
        if not self.is_spinning:
            self.is_spinning = True
            frame = self.frames[self.current_frame % len(self.frames)]
            sys.stdout.write(f"\r{frame} Processing...")
            sys.stdout.flush()
            self.current_frame += 1

    def finish(self, final_status: str) -> None:
        self.is_spinning = False
        sys.stdout.write(f"\r✓ {final_status}\n")
        sys.stdout.flush()


def main():
    client = anthropic.Anthropic()
    spinner = Spinner()

    print("Starting Claude API interaction with spinner...")

    try:
        spinner.spin()

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello from Claude!' and nothing else.",
                }
            ],
        )

        spinner.finish("API call completed successfully")

        response_text = message.content[0].text
        print(f"Response: {response_text}")

    except anthropic.APIError as e:
        spinner.finish(f"API Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()