from typing import List, Optional
from sqlalchemy.orm import Session
from models import User

class UserRepository:
    """User repository with database operations"""

    def get_all(self, db_session: Session, limit: int = 100) -> List[User]:
        return db_session.query(User).limit(limit).all()

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        return db_session.query(User).filter_by(id=user_id).first()

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        return db_session.query(User).filter_by(email=email).first()

    def create(self, name: str, email: str, db_session: Session) -> User:
        user = User(name=name, email=email)
        db_session.add(user)
        db_session.commit()
        return user

    def update(self, user_id: int, db_session: Session, **kwargs) -> Optional[User]:
        user = self.get_by_id(user_id, db_session)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db_session.commit()
        return user

    def delete(self, user_id: int, db_session: Session) -> bool:
        user = self.get_by_id(user_id, db_session)
        if user:
            db_session.delete(user)
            db_session.commit()
            return True
        return False