class DevopsCopilotCli:

    def __init__(self) -> None:
        pass

    def print_styled(self, content: str, style: str = ""):
        if style == "bold":
            print("\033[1m" + content + "\033[0m")
        elif style == "underline":
            print("\033[4m" + content + "\033[0m")
        else:
            print(content)