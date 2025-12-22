from cims.database.models import (
    Base,
    Resource as DbResource,
    Client as DbClient,
    ClientStatus as DbClientStatus,
    ProfileConfig as DbProfileConfig,
    PreRegister as DbPreRegister,
)

class _Clients:
    def refresh(self, tenant_id: int = 1) -> dict:
        session = get_session()
        clients = session.query(DbClient).filter_by(tenant_id=tenant_id).all()
        session.close()
        return {client.uid: client.client_id for client in clients}

    def register(self, uid: str, client_id: str, tenant_id: int = 1):
        session = get_session()
        client = session.query(DbClient).filter_by(tenant_id=tenant_id, uid=uid).first()
        if client:
            client.client_id = client_id
        else:
            client = DbClient(tenant_id=tenant_id, uid=uid, client_id=client_id)
            session.add(client)
        session.commit()
        ProfileConfig.register(uid, client_id, tenant_id)
        session.close()