class _Clients:
    def __init__(self):
        self._clients = {}

    def refresh(self, tenant_id: int = 1) -> dict:
        if tenant_id not in self._clients:
            self._clients[tenant_id] = {}
        return self._clients[tenant_id]

    def register(self, uid: str, client_id: str, tenant_id: int = 1):
        if tenant_id not in self._clients:
            self._clients[tenant_id] = {}
        self._clients[tenant_id][uid] = client_id