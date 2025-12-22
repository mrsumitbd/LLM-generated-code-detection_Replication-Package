class InstallationReport:
    
    def __init__(self, install_requirements: Sequence[InstallRequirement]):
        self.install_requirements = install_requirements

    @classmethod
    def _install_req_to_dict(cls, ireq: InstallRequirement) -> Dict[str, Any]:
        return {
            'name': ireq.name,
            'version': ireq.version,
            'extras': ireq.extras
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            'install_requirements': [self._install_req_to_dict(ireq) for ireq in self.install_requirements]
        }