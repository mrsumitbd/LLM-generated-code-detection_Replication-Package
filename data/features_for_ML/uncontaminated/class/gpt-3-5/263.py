from typing import Any

class Config:
    """Config for an imaginaire4 job.

    See /README.md/Configuration System for more info.
    """

    def pretty_print(self, use_color: bool = False) -> str:
        pass

    def to_dict(self) -> dict[str, Any]:
        pass

    def validate(self) -> None:
        pass