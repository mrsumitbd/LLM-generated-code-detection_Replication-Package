import json
from typing import Any as TypingAny, List, Union

class CommandGetDbSchemas:
    def __init__(self):
        self.schemas: List[str] = []

    def Unpack(self, any_message: TypingAny) -> None:
        """
        Unpack the incoming message into the internal schemas list.
        Supports dict, JSON string, bytes (JSON), and protobuf Any.
        """
        # Handle plain dictionary
        if isinstance(any_message, dict):
            self.schemas = any_message.get("schemas", [])
            return

        # Handle JSON string
        if isinstance(any_message, str):
            try:
                data = json.loads(any_message)
                self.schemas = data.get("schemas", [])
                return
            except json.JSONDecodeError:
                pass

        # Handle bytes (assumed to be JSON)
        if isinstance(any_message, (bytes, bytearray)):
            try:
                data = json.loads(any_message.decode("utf-8"))
                self.schemas = data.get("schemas", [])
                return
            except Exception:
                pass

        # Attempt to handle protobuf Any
        try:
            from google.protobuf.any_pb2 import Any as ProtobufAny
            if isinstance(any_message, ProtobufAny):
                # If we know the target type, we could unpack it here.
                # For now, store the Any object itself.
                self.schemas = [any_message]
                return
        except Exception:
            pass

        # Fallback: no schemas found
        self.schemas = []

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(schemas={self.schemas!r})"