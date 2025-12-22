from typing import Dict, Any, Optional, List
from sqlalchemy.orm import sessionmaker, Session, relationship

class UserRepository:
    """User repository with database operations"""

    def get_all(self, db_session: Session, limit: int = 100) -> List[User]:
        """Get all users with limit for performance"""
        return db_session.query(User).limit(limit).all()

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        """Get user by ID"""
        return db_session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        """Get user by email"""
        return db_session.query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, db_session: Session) -> User:
        """Create a new user"""
        user = User(name=name, email=email)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def update(self, user_id: int, db_session: Session, **kwargs) -> Optional[User]:
        """Update user"""
        user = self.get_by_id(user_id, db_session)
        if user:
            for key, value in kwargs.items():
                if value is not None and hasattr(user, key):
                    setattr(user, key, value)
            db_session.commit()
            return user
        return None

    def delete(self, user_id: int, db_session: Session) -> bool:
        """Delete user"""
        user = self.get_by_id(user_id, db_session)
        if user:
            db_session.delete(user)
            db_session.commit()
            return True
        return False