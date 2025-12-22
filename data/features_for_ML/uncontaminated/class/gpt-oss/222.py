from typing import List, Optional, Any
from sqlalchemy.orm import Session

# Assume the User model is defined elsewhere and imported here
from models import User


class UserRepository:
    """User repository with database operations"""

    def __init__(self) -> None:
        """Initialize the repository. No state is required."""
        pass

    def get_all(self, db_session: Session) -> List[User]:
        """Return all users in the database."""
        return db_session.query(User).all()

    def get_by_id(self, user_id: int, db_session: Session) -> Optional[User]:
        """Return a single user by primary key or None if not found."""
        return db_session.query(User).filter(User.id == user_id).one_or_none()

    def get_by_email(self, email: str, db_session: Session) -> Optional[User]:
        """Return a single user by email or None if not found."""
        return db_session.query(User).filter(User.email == email).one_or_none()

    def create(self, name: str, email: str, db_session: Session) -> User:
        """Create a new user and persist it to the database."""
        new_user = User(name=name, email=email)
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)
        return new_user

    def update(self, user_id: int, db_session: Session, **kwargs: Any) -> Optional[User]:
        """
        Update an existing user with the provided keyword arguments.
        Returns the updated user or None if the user does not exist.
        """
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
        """
        Delete a user by ID.
        Returns True if a user was deleted, False otherwise.
        """
        user = self.get_by_id(user_id, db_session)
        if not user:
            return False

        db_session.delete(user)
        db_session.commit()
        return True