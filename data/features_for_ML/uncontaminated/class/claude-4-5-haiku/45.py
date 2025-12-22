class SecurityManager:
    """
    Main security manager that manages authentication and authorization.
    """

    def __init__(self):
        self.authenticators = {}
        self.primary_auth_type = None
        self.unified_auth_manager = None
        self.auth_enabled = False
        self._initialize_authenticators()
        self._initialize_unified_auth_manager()
        self.primary_auth_type = self._determine_primary_auth_type()
        self.auth_enabled = self.validate_configuration()

    def _determine_primary_auth_type(self) -> str:
        if not self.authenticators:
            return None
        
        priority_order = ['oauth2', 'jwt', 'api_key', 'basic', 'custom']
        for auth_type in priority_order:
            if auth_type in self.authenticators:
                return auth_type
        
        return next(iter(self.authenticators.keys())) if self.authenticators else None

    def _initialize_authenticators(self) -> None:
        self.authenticators = {
            'basic': {'enabled': True, 'headers': {'Authorization'}},
            'api_key': {'enabled': True, 'headers': {'X-API-Key'}},
            'jwt': {'enabled': True, 'headers': {'Authorization'}},
            'oauth2': {'enabled': True, 'headers': {'Authorization'}},
        }

    def _initialize_unified_auth_manager(self) -> None:
        self.unified_auth_manager = {
            'enabled': True,
            'supported_types': list(self.authenticators.keys()),
            'default_type': self._determine_primary_auth_type()
        }

    def get_available_auth_types(self) -> set[str]:
        return set(auth_type for auth_type, config in self.authenticators.items() 
                   if config.get('enabled', False))

    def is_auth_enabled(self) -> bool:
        return self.auth_enabled

    def get_primary_auth_type(self) -> str:
        return self.primary_auth_type

    def get_required_headers(self, auth_type: str | None = None) -> set[str]:
        if auth_type is None:
            auth_type = self.primary_auth_type
        
        if auth_type not in self.authenticators:
            return set()
        
        return self.authenticators[auth_type].get('headers', set())

    def validate_configuration(self) -> bool:
        if not self.authenticators:
            return False
        
        available_types = self.get_available_auth_types()
        if not available_types:
            return False
        
        if self.primary_auth_type is None:
            return False
        
        if self.primary_auth_type not in available_types:
            return False
        
        primary_config = self.authenticators.get(self.primary_auth_type, {})
        if not primary_config.get('headers'):
            return False
        
        return True