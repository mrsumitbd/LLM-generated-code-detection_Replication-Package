class DevopsCopilotCli:
    def __init__(self) -> None:
        self.styles = {
            "bold": "\033[1m",
            "italic": "\033[3m",
            "underline": "\033[4m",
            "red": "\033[91m",
            "green": "\033[92m",
            "yellow": "\033[93m",
            "blue": "\033[94m",
            "magenta": "\033[95m",
            "cyan": "\033[96m",
            "white": "\033[97m",
            "reset": "\033[0m"
        }

    def print_styled(self, content: str, style: str = ""):
        styles = style.split(",")
        styled_content = "".join(self.styles.get(s, "") for s in styles) + content + self.styles["reset"]
        print(styled_content)