from typing import Any, Dict, List, Optional


class Session:
    """
    A simple session representation that can be persisted via a SessionManager.
    """

    def __init__(self, session_data: Optional[Dict[str, Any]] = None):
        """
        Initialize a Session instance.

        Parameters
        ----------
        session_data : dict, optional
            Existing session data to populate the instance. If omitted, an empty
            session is created.
        """
        # Base data that may come from a persistence layer
        self._data: Dict[str, Any] = dict(session_data or {})

        # Ensure core attributes exist
        self.commands: List[str] = self._data.get("commands", [])
        self.console: str = self._data.get("console", "")
        self.host_key: Optional[str] = self._data.get("host_key")
        self.processes_md5: Optional[str] = self._data.get("processes_md5")

    # --------------------------------------------------------------------- #
    #  Serialization helpers
    # --------------------------------------------------------------------- #
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the session into a plain dictionary suitable for persistence.
        """
        result: Dict[str, Any] = {
            "commands": list(self.commands),
            "console": self.console,
            "host_key": self.host_key,
            "processes_md5": self.processes_md5,
        }
        # Merge any additional data that was supplied during construction
        result.update(self._data)
        return result

    # --------------------------------------------------------------------- #
    #  Persistence helpers
    # --------------------------------------------------------------------- #
    def save(self, session_manager: "SessionManager") -> None:
        """
        Persist the current session using the provided session manager.

        The session manager is expected to expose a ``save_session`` method
        that accepts a Session instance.
        """
        if hasattr(session_manager, "save_session"):
            session_manager.save_session(self)
        else:
            raise AttributeError(
                "SessionManager must provide a 'save_session' method."
            )

    # --------------------------------------------------------------------- #
    #  Session mutation helpers
    # --------------------------------------------------------------------- #
    def add_command(self, command: str) -> None:
        """
        Append a command to the session's command history.
        """
        self.commands.append(command)

    def update_console(self, content: str) -> None:
        """
        Replace the console output stored in the session.
        """
        self.console = content

    def set_host_key(self, host_key: str, session_manager: "SessionManager") -> None:
        """
        Set the host key for the session and notify the session manager.
        """
        self.host_key = host_key
        if hasattr(session_manager, "update_session"):
            session_manager.update_session(self)

    def set_processes_md5(self, md5: str, session_manager: "SessionManager") -> None:
        """
        Set the MD5 hash of the processes list for the session and notify
        the session manager.
        """
        self.processes_md5 = md5
        if hasattr(session_manager, "update_session"):
            session_manager.update_session(self)