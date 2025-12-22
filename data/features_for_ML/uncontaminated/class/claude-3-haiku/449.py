class SLSSettings:
    """Settings for SLS related configuration.

    - endpoints: region -> host mapping
    - template: fallback when region not mapped
    """

    def __init__(self, endpoints: dict, template: str):
        self.endpoints = endpoints
        self.template = template

    def __post_init__(self):
        pass

    def resolve(self, region: str) -> str:
        if region in self.endpoints:
            return self.endpoints[region]
        else:
            return self.template.format(region=region)