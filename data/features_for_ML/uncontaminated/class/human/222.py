from typing import Dict, Any, Optional, List

class UserRepository:
    """User repository with database operations"""

    def __init__(self):
        print("👥 User repository initialized")

    def get_all(self, db_session: DatabaseSession) -> List[User]:
        """Get all users"""
        return db_session.get_session().query(User).all()

    def get_by_id(self, user_id: int, db_session: DatabaseSession) -> Optional[User]:
        """Get user by ID"""
        return db_session.get_session().query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str, db_session: DatabaseSession) -> Optional[User]:
        """Get user by email"""
        return db_session.get_session().query(User).filter(User.email == email).first()

    def create(self, name: str, email: str, db_session: DatabaseSession) -> User:
        """Create a new user"""
        user = User(name=name, email=email)
        with db_session.transaction():
            db_session.get_session().add(user)
            db_session.get_session().flush()  # To get the ID
        return user

    def update(self, user_id: int, db_session, **kwargs):
        """Update user with validated data"""
        user = db_session.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if value is not None and hasattr(user, key):
                    setattr(user, key, value)
            db_session.commit()
            return user
        return None

    def delete(self, user_id: int, db_session):
        """Delete user and return success status"""
        user = db_session.query(User).filter(User.id == user_id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
            return True
        return False