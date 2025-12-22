from typing import Any

class Config:
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    def __init__(self, **kwargs):
        self.config = kwargs

    def pretty_print(self, use_color: bool = False) -> str:
        output = ""
        for key, value in self.config.items():
            if use_color:
                output += f"\033[1m{key}\033[0m: {value}\n"
            else:
                output += f"{key}: {value}\n"
        return output.strip()

    def to_dict(self) -> dict[str, Any]:
        return self.config

    def validate(self) -> None:
        # Implement validation logic here
        pass