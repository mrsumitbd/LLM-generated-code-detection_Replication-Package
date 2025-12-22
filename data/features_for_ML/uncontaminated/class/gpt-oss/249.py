from __future__ import annotations

import datetime
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass(eq=True, frozen=True)
class RequestLogEntry:
    """
    Container for request log information.

    Attributes
    ----------
    timestamp : datetime.datetime
        The time the request was made.
    method : str
        HTTP method used for the request.
    url : str
        Full URL requested.
    status_code : int
        HTTP status code returned.
    response_time_ms : float
        Time taken to receive the response in milliseconds.
    request_headers : Optional[Dict[str, str]]
        Headers sent with the request.
    response_headers : Optional[Dict[str, str]]
        Headers received in the response.
    request_body : Optional[str]
        Body sent with the request.
    response_body : Optional[str]
        Body received in the response.
    """

    timestamp: datetime.datetime
    method: str
    url: str
    status_code: int
    response_time_ms: float
    request_headers: Optional[Dict[str, str]] = field(default_factory=dict)
    response_headers: Optional[Dict[str, str]] = field(default_factory=dict)
    request_body: Optional[str] = None
    response_body: Optional[str] = None

    def __post_init__(self) -> None:
        if not isinstance(self.timestamp, datetime.datetime):
            raise TypeError("timestamp must be a datetime.datetime instance")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the log entry to a plain dictionary suitable for JSON serialization.
        """
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestLogEntry":
        """
        Create a RequestLogEntry from a dictionary, parsing the timestamp.
        """
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.datetime.fromisoformat(timestamp)
        return cls(
            timestamp=timestamp,
            method=data["method"],
            url=data["url"],
            status_code=data["status_code"],
            response_time_ms=data["response_time_ms"],
            request_headers=data.get("request_headers", {}),
            response_headers=data.get("response_headers", {}),
            request_body=data.get("request_body"),
            response_body=data.get("response_body"),
        )

    def to_json(self) -> str:
        """
        Serialize the log entry to a JSON string.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "RequestLogEntry":
        """
        Deserialize a JSON string into a RequestLogEntry.
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self) -> str:
        return (
            f"{self.timestamp.isoformat()} | {self.method} {self.url} "
            f"-> {self.status_code} ({self.response_time_ms} ms)"
        )