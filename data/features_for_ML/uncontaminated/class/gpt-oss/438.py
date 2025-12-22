import re
from typing import Dict, Any, Optional


class CustomerInfo:
    """Customer informations."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        address: Optional[Dict[str, Any]] = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address or {}

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("Email must be a string")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email address")
        self._email = value

    @property
    def phone(self) -> Optional[str]:
        return self._phone

    @phone.setter
    def phone(self, value: Optional[str]) -> None:
        if value is None:
            self._phone = None
            return
        if not isinstance(value, str):
            raise TypeError("Phone must be a string")
        if not re.match(r"^[\d\-\+\s\(\)]+$", value):
            raise ValueError("Invalid phone number")
        self._phone = value

    @property
    def address(self) -> Dict[str, Any]:
        return self._address

    @address.setter
    def address(self, value: Dict[str, Any]) -> None:
        if not isinstance(value, dict):
            raise TypeError("Address must be a dict")
        self._address = value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CustomerInfo":
        return cls(
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            address=data.get("address"),
        )

    def __repr__(self) -> str:
        return (
            f"CustomerInfo({self.first_name!r}, {self.last_name!r}, "
            f"{self.email!r}, {self.phone!r}, {self.address!r})"
        )

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CustomerInfo):
            return False
        return self.to_dict() == other.to_dict()

    def update_email(self, new_email: str) -> None:
        self.email = new_email

    def update_phone(self, new_phone: str) -> None:
        self.phone = new_phone

    def update_address(self, new_address: Dict[str, Any]) -> None:
        self.address = new_address

    def mask_phone(self) -> Optional[str]:
        if not self.phone:
            return None
        digits = re.sub(r"\D", "", self.phone)
        masked = "*" * max(len(digits) - 4, 0) + digits[-4:]
        return masked

    def is_valid(self) -> bool:
        try:
            _ = self.email
            _ = self.phone
            return True
        except Exception:
            return False