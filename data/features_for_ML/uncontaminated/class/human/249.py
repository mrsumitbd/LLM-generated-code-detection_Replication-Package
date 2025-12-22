from typing import Any, Dict, Optional
from datetime import datetime, timezone

class RequestLogEntry:
    """Container for request log information"""

    timestamp: datetime
    method: str
    path: str
    status_code: int
    duration_ms: float
    response_size: int
    client_ip: str
    user_agent: Optional[str] = None
    error_message: Optional[str] = None
    query_params: Optional[str] = None