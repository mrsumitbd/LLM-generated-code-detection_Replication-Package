from dataclasses import dataclass
from typing import Dict

@dataclass
class SLSSettings:
    endpoints: Dict[str, str]
    template: str

    def __post_init__(self):
        self.endpoints = self.endpoints or {}
        self.template = self.template or ""

    def resolve(self, region: str) -> str:
        return self.endpoints.get(region, self.template)