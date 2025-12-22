def print_themed(text: str, style: str = "info") -> None:
    styles = {
        "info": "\033[94m",
        "success": "\033[92m",
        "warning": "\033[93m",
        "error": "\033[91m"
    }

    end_style = "\033[0m"

    if style in styles:
        print(styles[style] + text + end_style)
    else:
        print(text)