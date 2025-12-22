from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from easyswitch.types import (
    Currency, CustomerInfo, PaginationMeta, 
    Provider, TransactionDetail, TransactionStatus
)

class LogDetail:
    """Standardized log detail structure."""

    id: int
    method: str
    url: str
    status: str
    ip_address: str
    version: str
    provider: Provider
    source: str
    query: Optional[Dict[str, Any]] = None
    body: Optional[str] = None
    response: Optional[str] = None
    account_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_response: Dict[str, Any] = field(default_factory=dict)