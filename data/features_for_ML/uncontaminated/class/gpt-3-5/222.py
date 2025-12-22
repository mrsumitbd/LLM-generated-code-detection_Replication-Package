from typing import List, Optional

class UserRepository:
    """User repository with database operations"""

    def __init__(self):
        pass

    def get_all(self, db_session: DatabaseSession) -> List[User]:
        pass

    def get_by_id(self, user_id: int, db_session: DatabaseSession) -> Optional[User]:
        pass

    def get_by_email(self, email: str, db_session: DatabaseSession) -> Optional[User]:
        pass

    def create(self, name: str, email: str, db_session: DatabaseSession) -> User:
        pass

    def update(self, user_id: int, db_session, **kwargs):
        pass

    def delete(self, user_id: int, db_session):
        pass