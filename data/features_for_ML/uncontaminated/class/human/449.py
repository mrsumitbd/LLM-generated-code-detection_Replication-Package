from dataclasses import dataclass, field
from typing import Optional, Dict, Iterable

class SLSSettings:
    """Settings for SLS related configuration.

    - endpoints: region -> host mapping
    - template: fallback when region not mapped
    """

    endpoints: Dict[str, str] = field(default_factory=dict)
    template: str = "{region}.log.aliyuncs.com"

    def __post_init__(self):
        # normalize hosts
        normalized = {k: normalize_host(v) for k, v in (self.endpoints or {}).items()}
        object.__setattr__(self, "endpoints", normalized)

    def resolve(self, region: str) -> str:
        if not region:
            raise ValueError("region is required")
        host = self.endpoints.get(region)
        if host:
            return host
        return self.template.format(region=region)