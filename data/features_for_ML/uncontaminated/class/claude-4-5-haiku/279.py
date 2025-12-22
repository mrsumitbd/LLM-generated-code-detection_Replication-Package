from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class User:
    """User model"""
    def __init__(self, id: int = None, name: str = None, email: str = None):
        self.id = id
        self.name = name
        self.email = email


class UserRepository:
    """User repository with database operations"""

    def get_all(self, db_session: Session, limit: int = 100) -> List[User]:
        try:
            return db_session.query(User).limit(limit).all()
        except SQLAlchemyError:
            return []

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        try:
            return db_session.query(User).filter(User.id == user_id).first()
        except SQLAlchemyError:
            return None

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        try:
            return db_session.query(User).filter(User.email == email).first()
        except SQLAlchemyError:
            return None

    def create(self, name: str, email: str, db_session: Session) -> User:
        try:
            user = User(name=name, email=email)
            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except SQLAlchemyError:
            db_session.rollback()
            raise

    def update(self, user_id: int, db_session: Session, **kwargs) -> Optional[User]:
        try:
            user = db_session.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            db_session.commit()
            db_session.refresh(user)
            return user
        except SQLAlchemyError:
            db_session.rollback()
            return None

    def delete(self, user_id: int, db_session: Session) -> bool:
        try:
            user = db_session.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            
            db_session.delete(user)
            db_session.commit()
            return True
        except SQLAlchemyError:
            db_session.rollback()
            return False