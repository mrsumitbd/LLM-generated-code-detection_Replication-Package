from dataclasses import dataclass, field
from typing import Dict


@dataclass
class SLSSettings:
    """Settings for SLS related configuration.

    - endpoints: region -> host mapping
    - template: fallback when region not mapped
    """
    endpoints: Dict[str, str] = field(default_factory=dict)
    template: str = "sls.{region}.aliyuncs.com"

    def __post_init__(self) -> None:
        if not isinstance(self.endpoints, dict):
            raise TypeError("`endpoints` must be a dictionary")
        if not isinstance(self.template, str):
            raise TypeError("`template` must be a string")

    def resolve(self, region: str) -> str:
        """Return the host for the given region.

        If the region is present in :attr:`endpoints`, its value is returned.
        Otherwise the :attr:`template` is used to generate the host.
        """
        if region in self.endpoints:
            return self.endpoints[region]

        if not self.template:
            raise ValueError(f"No endpoint found for region '{region}' and no template provided")

        try:
            return self.template.format(region=region)
        except Exception as exc:
            raise ValueError(
                f"Failed to format template '{self.template}' with region '{region}'"
            ) from exc