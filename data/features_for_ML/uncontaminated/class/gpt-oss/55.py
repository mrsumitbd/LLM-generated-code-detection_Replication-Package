import threading
from copy import deepcopy
from typing import Dict


class _Clients:
    """
    Simple in‑memory client registry per tenant.
    """

    def __init__(self) -> None:
        # Mapping: tenant_id -> {uid: client_id}
        self._registry: Dict[int, Dict[str, str]] = {}
        self._lock = threading.RLock()

    def refresh(self, tenant_id: int = 1) -> dict:
        """
        Return a copy of the client mapping for the given tenant.
        """
        with self._lock:
            return deepcopy(self._registry.get(tenant_id, {}))

    def register(self, uid: str, client_id: str, tenant_id: int = 1) -> None:
        """
        Register a new client for the specified tenant.
        Raises ValueError if the uid is already registered for that tenant.
        """
        with self._lock:
            tenant_map = self._registry.setdefault(tenant_id, {})
            if uid in tenant_map:
                raise ValueError(
                    f"UID '{uid}' is already registered for tenant {tenant_id}"
                )
            tenant_map[uid] = client_id