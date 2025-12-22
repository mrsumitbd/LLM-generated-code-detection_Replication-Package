from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class WebhookEvent:
    """Standardized webhook event structure."""

    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime.datetime | str
    signature: Optional[str] = None
    headers: Optional[Dict[str, str]] = None
    event_id: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.datetime.fromisoformat(self.timestamp)
            except ValueError:
                # Try common formats
                for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"):
                    try:
                        self.timestamp = datetime.datetime.strptime(self.timestamp, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Invalid timestamp format: {self.timestamp}")

        if not isinstance(self.payload, dict):
            raise TypeError("payload must be a dict")

        if self.headers is not None and not isinstance(self.headers, dict):
            raise TypeError("headers must be a dict if provided")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WebhookEvent":
        """Create an event from a dictionary, handling common key variations."""
        event_type = data.get("event_type") or data.get("type") or data.get("event")
        if event_type is None:
            raise KeyError("Missing event_type in data")

        payload = data.get("payload") or data.get("data") or data
        if isinstance(payload, dict) and "payload" in payload:
            payload = payload["payload"]

        timestamp = data.get("timestamp") or data.get("time") or data.get("created_at")
        if timestamp is None:
            raise KeyError("Missing timestamp in data")

        signature = data.get("signature")
        headers = data.get("headers")
        event_id = data.get("event_id") or data.get("id")

        return cls(
            event_type=event_type,
            payload=payload,
            timestamp=timestamp,
            signature=signature,
            headers=headers,
            event_id=event_id,
        )

    @classmethod
    def from_json(cls, json_str: str) -> "WebhookEvent":
        """Create an event from a JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serializable dictionary representation."""
        return {
            "event_type": self.event_type,
            "payload": self.payload,
            "timestamp": (
                self.timestamp.isoformat()
                if isinstance(self.timestamp, datetime.datetime)
                else self.timestamp
            ),
            "signature": self.signature,
            "headers": self.headers,
            "event_id": self.event_id,
        }

    def to_json(self, indent: Optional[int] = None) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict(), indent=indent)

    def to_bytes(self) -> bytes:
        """Return the event as UTF‑8 encoded bytes."""
        return self.to_json().encode("utf-8")

    def to_base64(self) -> str:
        """Return the event as a base64 encoded string."""
        return base64.b64encode(self.to_bytes()).decode("utf-8")

    def pretty_json(self) -> str:
        """Return a pretty‑printed JSON string."""
        return json.dumps(self.to_dict(), indent=4, sort_keys=True)

    def validate(self) -> bool:
        """Basic validation of required fields."""
        if not isinstance(self.event_type, str) or not self.event_type:
            return False
        if not isinstance(self.payload, dict):
            return False
        if not isinstance(self.timestamp, datetime.datetime):
            return False
        return True

    def verify_signature(self, secret: str, algorithm: str = "sha256") -> bool:
        """
        Verify the HMAC signature of the payload.

        Parameters
        ----------
        secret : str
            The shared secret used to compute the HMAC.
        algorithm : str, optional
            The hash algorithm to use ('sha256' or 'sha1'). Defaults to 'sha256'.

        Returns
        -------
        bool
            True if the signature matches, False otherwise.
        """
        if not self.signature:
            return False

        payload_bytes = json.dumps(
            self.payload, separators=(",", ":"), sort_keys=True
        ).encode("utf-8")

        algo = algorithm.lower()
        if algo == "sha256":
            digest = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()
        elif algo == "sha1":
            digest = hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha1).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        return hmac.compare_digest(digest, self.signature)

    def get_header(self, key: str) -> Optional[str]:
        """Retrieve a header value by key."""
        return self.headers.get(key) if self.headers else None

    def __repr__(self) -> str:
        ts = (
            self.timestamp.isoformat()
            if isinstance(self.timestamp, datetime.datetime)
            else self.timestamp
        )
        return (
            f"<WebhookEvent type={self.event_type!r} "
            f"id={self.event_id!r} timestamp={ts!r}>"
        )