from typing import Literal

def extract_simple(
    file_path: str,
    mime_type: str | None = None,
    response_format: Literal["text", "markdown"] = "text",
) -> str:
    try:
        with open(file_path, "r") as file:
            content = file.read()

        if response_format == "markdown":
            return f"```\n{content}\n```"
        else:
            return content
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"Error: {str(e)}"