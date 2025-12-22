from typing import List, Optional
from database import DatabaseSession
from models import User

class UserRepository:
    """User repository with database operations"""

    def __init__(self):
        pass

    def get_all(self, db_session: DatabaseSession) -> List[User]:
        return db_session.query(User).all()

    def get_by_id(self, user_id: int, db_session: DatabaseSession) -> Optional[User]:
        return db_session.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str, db_session: DatabaseSession) -> Optional[User]:
        return db_session.query(User).filter_by(email=email).first()

    def create(self, name: str, email: str, db_session: DatabaseSession) -> User:
        user = User(name=name, email=email)
        db_session.add(user)
        db_session.commit()
        return user

    def update(self, user_id: int, db_session, **kwargs):
        user = self.get_by_id(user_id, db_session)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db_session.commit()

    def delete(self, user_id: int, db_session):
        user = self.get_by_id(user_id, db_session)
        if user:
            db_session.delete(user)
            db_session.commit()