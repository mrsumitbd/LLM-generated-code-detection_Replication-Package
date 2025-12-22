from typing import List, Optional

from sqlalchemy.orm import Session

from .models import User  # adjust import path as needed


class UserRepository:
    """User repository with database operations"""

    def get_all(self, db_session: Session, limit: int = 100) -> List[User]:
        """Return a list of users up to the specified limit."""
        return db_session.query(User).limit(limit).all()

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        """Return a single user by primary key or None if not found."""
        return db_session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        """Return a single user by email or None if not found."""
        return db_session.query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, db_session: Session) -> User:
        """Create a new user record and return the created instance."""
        new_user = User(name=name, email=email)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user

    def update(self, user_id: int, db_session: Session, **kwargs) -> Optional[User]:
        """Update an existing user with provided keyword arguments."""
        user = self.get_by_id(user_id, db_session)
        if not user:
            return None
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db_session.commit()
        db_session.refresh(user)
        return user

    def delete(self, user_id: int, db_session: Session) -> bool:
        """Delete a user by ID. Returns True if deletion succeeded."""
        user = self.get_by_id(user_id, db_session)
        if not user:
            return False
        db_session.delete(user)
        db_session.commit()
        return True