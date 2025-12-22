import json
import os
from typing import Dict, Optional, Any, Iterable


class CommandsCfg:
    """Command terms for the MDP."""

    _DEFAULT_COMMANDS: Dict[str, Dict[str, Any]] = {
        "move": {"id": 1, "description": "Move forward"},
        "turn_left": {"id": 2, "description": "Turn left"},
        "turn_right": {"id": 3, "description": "Turn right"},
        "pick": {"id": 4, "description": "Pick up object"},
        "drop": {"id": 5, "description": "Drop object"},
    }

    def __init__(self, commands: Optional[Dict[str, Dict[str, Any]]] = None) -> None:
        """
        Initialize the CommandsCfg instance.

        Parameters
        ----------
        commands : Optional[Dict[str, Dict[str, Any]]]
            A dictionary mapping command names to their attributes.
            If None, the default commands are used.
        """
        if commands is None:
            self._commands = dict(self._DEFAULT_COMMANDS)
        else:
            self._commands = dict(commands)

    def add_command(
        self,
        name: str,
        *,
        id: Optional[int] = None,
        description: Optional[str] = None,
        **extra: Any,
    ) -> None:
        """
        Add a new command or update an existing one.

        Parameters
        ----------
        name : str
            The command name.
        id : Optional[int]
            The command identifier.
        description : Optional[str]
            A textual description of the command.
        **extra : Any
            Any additional attributes to store.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("Command name must be a non-empty string.")
        cmd = {"id": id, "description": description}
        cmd.update(extra)
        self._commands[name] = cmd

    def remove_command(self, name: str) -> None:
        """
        Remove a command by name.

        Parameters
        ----------
        name : str
            The command name to remove.
        """
        if name in self._commands:
            del self._commands[name]
        else:
            raise KeyError(f"Command '{name}' not found.")

    def get_command(self, name: str) -> Dict[str, Any]:
        """
        Retrieve the attributes of a command.

        Parameters
        ----------
        name : str
            The command name.

        Returns
        -------
        Dict[str, Any]
            The command attributes.
        """
        try:
            return self._commands[name]
        except KeyError:
            raise KeyError(f"Command '{name}' not found.") from None

    def list_commands(self) -> Iterable[str]:
        """Return an iterable of command names."""
        return iter(self._commands)

    def to_dict(self) -> Dict[str, Dict[str, Any]]:
        """Return a deep copy of the internal command dictionary."""
        return {k: dict(v) for k, v in self._commands.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Dict[str, Any]]) -> "CommandsCfg":
        """
        Create a CommandsCfg instance from a dictionary.

        Parameters
        ----------
        data : Dict[str, Dict[str, Any]]
            The command dictionary.

        Returns
        -------
        CommandsCfg
        """
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary.")
        return cls(commands=data)

    def to_json(self, file_path: str, *, indent: Optional[int] = 4) -> None:
        """
        Serialize the command configuration to a JSON file.

        Parameters
        ----------
        file_path : str
            Path to the output file.
        indent : Optional[int]
            Indentation level for pretty printing.
        """
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=indent)

    @classmethod
    def from_json(cls, file_path: str) -> "CommandsCfg":
        """
        Load a CommandsCfg instance from a JSON file.

        Parameters
        ----------
        file_path : str
            Path to the JSON file.

        Returns
        -------
        CommandsCfg
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    def __contains__(self, name: str) -> bool:
        return name in self._commands

    def __iter__(self):
        return iter(self._commands)

    def __len__(self) -> int:
        return len(self._commands)

    def __repr__(self) -> str:
        cmd_names = ", ".join(sorted(self._commands))
        return f"{self.__class__.__name__}({cmd_names})"