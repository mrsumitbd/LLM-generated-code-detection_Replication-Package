from typing import Dict, List, Any, Optional, Set
from wazuh_mcp_server.config import ComplianceFramework

class ComplianceRequirement:
    """Individual compliance requirement."""
    id: str
    title: str
    description: str
    framework: ComplianceFramework
    status: ComplianceStatus
    score: float  # 0-100
    evidence: List[str]
    gaps: List[str]
    recommendations: List[str]