from typing import Sequence, Dict, Any
from dataclasses import dataclass

@dataclass
class InstallRequirement:
    name: str
    version: str
    is_satisfied: bool

class InstallationReport:
    def __init__(self, install_requirements: Sequence[InstallRequirement]):
        self.install_requirements = install_requirements

    @classmethod
    def _install_req_to_dict(cls, ireq: InstallRequirement) -> Dict[str, Any]:
        return {
            "name": ireq.name,
            "version": ireq.version,
            "is_satisfied": ireq.is_satisfied
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "install_requirements": [self._install_req_to_dict(req) for req in self.install_requirements]
        }