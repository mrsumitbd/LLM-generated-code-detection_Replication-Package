import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Union


class SessionData:
    """Data entry for a terminal session."""

    def __init__(
        self,
        session_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.session_id: str = session_id or str(uuid.uuid4())
        self.start_time: datetime = start_time or datetime.now(timezone.utc)
        self.end_time: Optional[datetime] = None
        self.commands: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = metadata or {}

    # ------------------------------------------------------------------
    # Context manager support
    # ------------------------------------------------------------------
    def __enter__(self) -> "SessionData":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Core functionality
    # ------------------------------------------------------------------
    def add_command(
        self,
        command: str,
        output: Optional[str] = None,
        *,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record a command and its optional output."""
        entry: Dict[str, Any] = {
            "command": command,
            "output": output,
            "timestamp": datetime.now(timezone.utc),
        }
        if metadata:
            entry["metadata"] = metadata
        self.commands.append(entry)

    def close(self, end_time: Optional[datetime] = None) -> None:
        """Mark the session as finished."""
        self.end_time = end_time or datetime.now(timezone.utc)

    @property
    def duration(self) -> Optional[float]:
        """Return the duration of the session in seconds, or None if not closed."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def __len__(self) -> int:
        return len(self.commands)

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        return iter(self.commands)

    def __contains__(self, command: str) -> bool:
        return any(entry["command"] == command for entry in self.commands)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        return self.commands[index]

    def __repr__(self) -> str:
        return (
            f"<SessionData id={self.session_id!r} "
            f"commands={len(self.commands)} "
            f"started={self.start_time.isoformat()} "
            f"ended={self.end_time.isoformat() if self.end_time else None}>"
        )

    def __str__(self) -> str:
        lines = [
            f"Session ID: {self.session_id}",
            f"Start: {self.start_time.isoformat()}",
            f"End: {self.end_time.isoformat() if self.end_time else 'ongoing'}",
            f"Duration: {self.duration:.2f}s" if self.duration else "Duration: ongoing",
            f"Commands: {len(self.commands)}",
        ]
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the session to a plain dictionary."""
        return {
            "session_id": self.session_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "commands": [
                {
                    "command": cmd["command"],
                    "output": cmd.get("output"),
                    "timestamp": cmd["timestamp"].isoformat(),
                    "metadata": cmd.get("metadata"),
                }
                for cmd in self.commands
            ],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SessionData":
        """Create a SessionData instance from a dictionary."""
        session = cls(
            session_id=data.get("session_id"),
            start_time=datetime.fromisoformat(data["start_time"]),
            metadata=data.get("metadata", {}),
        )
        if data.get("end_time"):
            session.end_time = datetime.fromisoformat(data["end_time"])
        for cmd in data.get("commands", []):
            session.commands.append(
                {
                    "command": cmd["command"],
                    "output": cmd.get("output"),
                    "timestamp": datetime.fromisoformat(cmd["timestamp"]),
                    "metadata": cmd.get("metadata"),
                }
            )
        return session

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------
    def set_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default: Any = None) -> Any:
        return self.metadata.get(key, default)

    def clear_metadata(self) -> None:
        self.metadata.clear()

    # ------------------------------------------------------------------
    # Command query helpers
    # ------------------------------------------------------------------
    def get_commands(self) -> List[Dict[str, Any]]:
        return self.commands

    def get_outputs(self) -> List[Optional[str]]:
        return [cmd.get("output") for cmd in self.commands]

    def get_last_output(self) -> Optional[str]:
        if not self.commands:
            return None
        return self.commands[-1].get("output")

    def get_commands_between(
        self,
        start: datetime,
        end: datetime,
    ) -> List[Dict[str, Any]]:
        return [
            cmd
            for cmd in self.commands
            if start <= cmd["timestamp"] <= end
        ]

    def get_output_by_command(self, command: str) -> List[Optional[str]]:
        return [cmd.get("output") for cmd in self.commands if cmd["command"] == command]