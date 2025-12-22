from __future__ import annotations

import datetime
import json
import logging
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional, Tuple, Union


@dataclass(frozen=True)
class LogDetail:
    """
    Standardized log detail structure.

    Attributes
    ----------
    timestamp : datetime.datetime
        The time the log entry was created. Defaults to UTC now.
    level : str
        Logging level name (e.g., "INFO", "ERROR"). Stored in upper case.
    message : str
        The log message.
    logger_name : Optional[str]
        Name of the logger that produced the log. Optional.
    module : Optional[str]
        Module name where the log was emitted. Optional.
    function : Optional[str]
        Function name where the log was emitted. Optional.
    line_no : Optional[int]
        Line number in the source file where the log was emitted. Optional.
    exc_info : Optional[Union[Tuple[type, BaseException, Any], str]]
        Exception information if the log was generated from an exception.
        Can be a tuple as returned by ``sys.exc_info()`` or a string.
    extra : Dict[str, Any]
        Additional context data.
    """

    timestamp: datetime.datetime = field(default_factory=lambda: datetime.datetime.utcnow())
    level: str = "INFO"
    message: str = ""
    logger_name: Optional[str] = None
    module: Optional[str] = None
    function: Optional[str] = None
    line_no: Optional[int] = None
    exc_info: Optional[Union[Tuple[type, BaseException, Any], str]] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Ensure timestamp is a datetime instance
        if not isinstance(self.timestamp, datetime.datetime):
            raise TypeError("timestamp must be a datetime.datetime instance")

        # Normalize level to upper case
        object.__setattr__(self, "level", self.level.upper())

        # Validate level against known logging levels
        valid_levels = {
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
            "NOTSET",
        }
        if self.level not in valid_levels:
            raise ValueError(f"Invalid logging level: {self.level}")

        # Ensure exc_info is either None, a tuple, or a string
        if self.exc_info is not None and not (
            isinstance(self.exc_info, tuple)
            or isinstance(self.exc_info, str)
        ):
            raise TypeError("exc_info must be a tuple or a string")

        # Ensure extra is a dict
        if not isinstance(self.extra, dict):
            raise TypeError("extra must be a dict")

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary representation suitable for JSON serialization."""
        data = asdict(self)
        # Convert datetime to ISO format
        data["timestamp"] = self.timestamp.isoformat()
        # Convert exc_info tuple to string if present
        if isinstance(self.exc_info, tuple):
            exc_type, exc_value, exc_traceback = self.exc_info
            data["exc_info"] = {
                "type": exc_type.__name__,
                "value": str(exc_value),
                "traceback": "".join(
                    logging.Formatter().formatException(self.exc_info)
                ),
            }
        return data

    def to_json(self, *, indent: Optional[int] = None) -> str:
        """Return a JSON string representation of the log detail."""
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogDetail":
        """Create a LogDetail instance from a dictionary."""
        # Parse timestamp
        ts = data.get("timestamp")
        if isinstance(ts, str):
            ts = datetime.datetime.fromisoformat(ts)
        elif not isinstance(ts, datetime.datetime):
            ts = datetime.datetime.utcnow()

        # Parse exc_info
        exc = data.get("exc_info")
        if isinstance(exc, dict):
            exc = (
                getattr(logging, exc.get("type", "Exception")),
                Exception(exc.get("value", "")),
                None,
            )

        return cls(
            timestamp=ts,
            level=data.get("level", "INFO"),
            message=data.get("message", ""),
            logger_name=data.get("logger_name"),
            module=data.get("module"),
            function=data.get("function"),
            line_no=data.get("line_no"),
            exc_info=exc,
            extra=data.get("extra", {}),
        )

    @classmethod
    def from_log_record(cls, record: logging.LogRecord) -> "LogDetail":
        """Create a LogDetail instance from a standard logging.LogRecord."""
        exc = None
        if record.exc_info:
            exc = record.exc_info
        return cls(
            timestamp=datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc),
            level=record.levelname,
            message=record.getMessage(),
            logger_name=record.name,
            module=record.module,
            function=record.funcName,
            line_no=record.lineno,
            exc_info=exc,
            extra=record.__dict__.get("extra", {}),
        )

    def __str__(self) -> str:
        """Human‑readable string representation."""
        parts = [
            f"[{self.timestamp.isoformat()}]",
            f"{self.level}",
            f"{self.logger_name or 'root'}",
            f"{self.message}",
        ]
        if self.exc_info:
            parts.append(f"Exception: {self.exc_info}")
        if self.extra:
            parts.append(f"Extra: {self.extra}")
        return " | ".join(parts)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"timestamp={self.timestamp!r}, "
            f"level={self.level!r}, "
            f"message={self.message!r}, "
            f"logger_name={self.logger_name!r}, "
            f"module={self.module!r}, "
            f"function={self.function!r}, "
            f"line_no={self.line_no!r}, "
            f"exc_info={self.exc_info!r}, "
            f"extra={self.extra!r})"
        )