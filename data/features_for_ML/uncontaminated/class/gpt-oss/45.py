import os
from typing import Dict, Set, Optional


class SecurityManager:
    """
    Main security manager that manages authentication and authorization.
    """

    def __init__(self):
        # Load configuration from environment or use defaults
        self._config: Dict[str, object] = {
            "auth_enabled": os.getenv("AUTH_ENABLED", "true").lower() == "true",
            "auth_types": os.getenv("AUTH_TYPES", "basic,token").split(","),
            "auth_requirements": {
                "basic": {"Authorization"},
                "token": {"Authorization"},
                "oauth": {"Authorization"},
            },
        }
        self._authenticators: Dict[str, object] = {}
        self._unified_auth_manager: Optional[object] = None
        self._primary_auth_type: Optional[str] = None

        self._initialize_authenticators()
        self._initialize_unified_auth_manager()
        self._primary_auth_type = self._determine_primary_auth_type()

    def _determine_primary_auth_type(self) -> str:
        """
        Determine the primary authentication type.
        The first enabled auth type in the configured list is chosen.
        """
        if not self.is_auth_enabled():
            raise RuntimeError("Authentication is disabled; no primary auth type.")
        for auth_type in self.get_available_auth_types():
            if auth_type in self._authenticators:
                return auth_type
        raise RuntimeError("No valid authentication type found.")

    def _initialize_authenticators(self) -> None:
        """
        Initialize authenticator instances for each configured auth type.
        For demonstration purposes, authenticators are simple placeholders.
        """
        for auth_type in self.get_available_auth_types():
            # Placeholder authenticator object
            self._authenticators[auth_type] = {"type": auth_type, "handler": None}

    def _initialize_unified_auth_manager(self) -> None:
        """
        Initialize a unified authentication manager that aggregates all authenticators.
        """
        self._unified_auth_manager = {
            "authenticators": list(self._authenticators.values())
        }

    def get_available_auth_types(self) -> Set[str]:
        """
        Return the set of authentication types configured.
        """
        return set(self._config.get("auth_types", []))

    def is_auth_enabled(self) -> bool:
        """
        Return whether authentication is enabled.
        """
        return bool(self._config.get("auth_enabled", False))

    def get_primary_auth_type(self) -> str:
        """
        Return the primary authentication type.
        """
        if self._primary_auth_type is None:
            self._primary_auth_type = self._determine_primary_auth_type()
        return self._primary_auth_type

    def get_required_headers(self, auth_type: Optional[str] = None) -> Set[str]:
        """
        Return the set of required headers for the specified authentication type.
        If no type is specified, use the primary authentication type.
        """
        if auth_type is None:
            auth_type = self.get_primary_auth_type()
        requirements = self._config.get("auth_requirements", {})
        return requirements.get(auth_type, set())

    def validate_configuration(self) -> bool:
        """
        Validate that the configuration is coherent:
        - Authentication must be enabled if any auth types are configured.
        - Each auth type must have at least one required header.
        """
        if not self.is_auth_enabled() and self.get_available_auth_types():
            return False
        for auth_type in self.get_available_auth_types():
            headers = self.get_required_headers(auth_type)
            if not headers:
                return False
        return True