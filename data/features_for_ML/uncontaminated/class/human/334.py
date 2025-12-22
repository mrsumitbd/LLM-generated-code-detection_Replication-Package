from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime

class WebhookEvent:
    """Standardized webhook event structure."""

    event_type: str
    provider: Provider
    transaction_id: str
    status: TransactionStatus
    amount: float
    currency: Currency
    created_at: Optional[datetime] = None
    raw_data: Dict[str, Any] = field(default_factory = dict)
    metadata: Dict[str, Any] = field(default_factory = dict)
    context: Dict[str,Any] = field(default_factory = dict)