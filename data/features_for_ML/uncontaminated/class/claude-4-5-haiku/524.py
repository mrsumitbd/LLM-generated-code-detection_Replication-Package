class BuildConfiguration:
    """Configuration for a PCILeech firmware build."""

    def __init__(self, **kwargs):
        self._config = kwargs

    @property
    def is_advanced(self) -> bool:
        return any(key.startswith('_') or key not in ['name', 'version', 'target'] 
                   for key in self._config.keys())

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._config)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BuildConfiguration":
        return cls(**data)