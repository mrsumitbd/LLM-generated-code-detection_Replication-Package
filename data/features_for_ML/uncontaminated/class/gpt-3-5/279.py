from typing import List, Optional
from sqlalchemy.orm import Session

class UserRepository:
    """User repository with database operations"""

    def get_all(self, db_session: Session, limit: int = 100) -> List[User]:
        return db_session.query(User).limit(limit).all()

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        return db_session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        return db_session.query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, db_session: Session) -> User:
        new_user = User(name=name, email=email)
        db_session.add(new_user)
        db_session.commit()
        return new_user

    def update(self, user_id: int, db_session: Session, **kwargs) -> Optional[User]:
        user = db_session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            db_session.commit()
            return user
        return None

    def delete(self, user_id: int, db_session: Session) -> bool:
        user = db_session.query(User).filter(User.id == user_id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
            return True
        return False