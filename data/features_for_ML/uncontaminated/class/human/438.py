from dataclasses import dataclass, field
from typing import Any, Dict, Optional

class CustomerInfo:
    """Customer informations."""

    phone_number: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    zip_code: Optional[str] = None
    state: Optional[str] = None
    id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)