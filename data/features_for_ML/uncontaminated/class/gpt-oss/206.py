from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional, Tuple, Union


@dataclass(frozen=True)
class BatchAction:
    """
    Represents a single action that can be included in a NEAR promise batch.

    The class supports the most common NEAR actions and provides convenient
    constructors, validation, and JSON serialization helpers.

    Attributes
    ----------
    action_type : str
        The type of the action (e.g. "Transfer", "FunctionCall", etc.).
    params : Mapping[str, Any]
        Parameters specific to the action type.
    """

    action_type: str
    params: Mapping[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Construction helpers
    # ------------------------------------------------------------------
    @classmethod
    def transfer(cls, amount: int) -> "BatchAction":
        """Create a transfer action."""
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("amount must be a non‑negative integer")
        return cls("Transfer", {"amount": amount})

    @classmethod
    def function_call(
        cls,
        method_name: str,
        args: Mapping[str, Any],
        gas: int,
        deposit: int,
    ) -> "BatchAction":
        """Create a function call action."""
        if not isinstance(method_name, str) or not method_name:
            raise ValueError("method_name must be a non‑empty string")
        if not isinstance(args, Mapping):
            raise ValueError("args must be a mapping")
        if not isinstance(gas, int) or gas <= 0:
            raise ValueError("gas must be a positive integer")
        if not isinstance(deposit, int) or deposit < 0:
            raise ValueError("deposit must be a non‑negative integer")
        return cls(
            "FunctionCall",
            {
                "method_name": method_name,
                "args": args,
                "gas": gas,
                "deposit": deposit,
            },
        )

    @classmethod
    def stake(cls, stake: int, public_key: str) -> "BatchAction":
        """Create a stake action."""
        if not isinstance(stake, int) or stake <= 0:
            raise ValueError("stake must be a positive integer")
        if not isinstance(public_key, str) or not public_key:
            raise ValueError("public_key must be a non‑empty string")
        return cls("Stake", {"stake": stake, "public_key": public_key})

    @classmethod
    def add_key(cls, public_key: str, access_key: Mapping[str, Any]) -> "BatchAction":
        """Create an add key action."""
        if not isinstance(public_key, str) or not public_key:
            raise ValueError("public_key must be a non‑empty string")
        if not isinstance(access_key, Mapping):
            raise ValueError("access_key must be a mapping")
        return cls("AddKey", {"public_key": public_key, "access_key": access_key})

    @classmethod
    def delete_key(cls, public_key: str) -> "BatchAction":
        """Create a delete key action."""
        if not isinstance(public_key, str) or not public_key:
            raise ValueError("public_key must be a non‑empty string")
        return cls("DeleteKey", {"public_key": public_key})

    @classmethod
    def delete_account(cls, beneficiary_id: str) -> "BatchAction":
        """Create a delete account action."""
        if not isinstance(beneficiary_id, str) or not beneficiary_id:
            raise ValueError("beneficiary_id must be a non‑empty string")
        return cls("DeleteAccount", {"beneficiary_id": beneficiary_id})

    # ------------------------------------------------------------------
    # Serialization helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        """Return a plain dictionary representation."""
        return {"action_type": self.action_type, "params": dict(self.params)}

    def to_json(self) -> str:
        """Return a JSON string representation."""
        return json.dumps(self.to_dict(), separators=(",", ":"))

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "BatchAction":
        """Create an instance from a dictionary."""
        action_type = data.get("action_type")
        if not isinstance(action_type, str):
            raise ValueError("action_type must be a string")
        params = data.get("params", {})
        if not isinstance(params, Mapping):
            raise ValueError("params must be a mapping")
        return cls(action_type, params)

    @classmethod
    def from_json(cls, json_str: str) -> "BatchAction":
        """Create an instance from a JSON string."""
        data = json.loads(json_str)
        if not isinstance(data, Mapping):
            raise ValueError("JSON must represent an object")
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    # Convenience methods
    # ------------------------------------------------------------------
    def __repr__(self) -> str:
        return f"BatchAction(action_type={self.action_type!r}, params={dict(self.params)!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BatchAction):
            return NotImplemented
        return self.action_type == other.action_type and dict(self.params) == dict(other.params)

    def __hash__(self) -> int:
        return hash((self.action_type, tuple(sorted(self.params.items()))))

    # ------------------------------------------------------------------
    # Validation on construction
    # ------------------------------------------------------------------
    def __post_init__(self):
        # Basic validation for known action types
        if self.action_type == "Transfer":
            amount = self.params.get("amount")
            if not isinstance(amount, int) or amount < 0:
                raise ValueError("Transfer action requires a non‑negative integer amount")
        elif self.action_type == "FunctionCall":
            method_name = self.params.get("method_name")
            args = self.params.get("args")
            gas = self.params.get("gas")
            deposit = self.params.get("deposit")
            if not isinstance(method_name, str) or not method_name:
                raise ValueError("FunctionCall requires a non‑empty method_name")
            if not isinstance(args, Mapping):
                raise ValueError("FunctionCall requires args to be a mapping")
            if not isinstance(gas, int) or gas <= 0:
                raise ValueError("FunctionCall requires a positive gas")
            if not isinstance(deposit, int) or deposit < 0:
                raise ValueError("FunctionCall requires a non‑negative deposit")
        elif self.action_type == "Stake":
            stake = self.params.get("stake")
            public_key = self.params.get("public_key")
            if not isinstance(stake, int) or stake <= 0:
                raise ValueError("Stake requires a positive stake")
            if not isinstance(public_key, str) or not public_key:
                raise ValueError("Stake requires a non‑empty public_key")
        elif self.action_type == "AddKey":
            public_key = self.params.get("public_key")
            access_key = self.params.get("access_key")
            if not isinstance(public_key, str) or not public_key:
                raise ValueError("AddKey requires a non‑empty public_key")
            if not isinstance(access_key, Mapping):
                raise ValueError("AddKey requires access_key to be a mapping")
        elif self.action_type == "DeleteKey":
            public_key = self.params.get("public_key")
            if not isinstance(public_key, str) or not public_key:
                raise ValueError("DeleteKey requires a non‑empty public_key")
        elif self.action_type == "DeleteAccount":
            beneficiary_id = self.params.get("beneficiary_id")
            if not isinstance(beneficiary_id, str) or not beneficiary_id:
                raise ValueError("DeleteAccount requires a non‑empty beneficiary_id")
        else:
            # Unknown action types are allowed but no validation is performed
            pass