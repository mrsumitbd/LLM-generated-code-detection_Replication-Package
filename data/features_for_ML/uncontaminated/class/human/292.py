from typing import Dict, Any, Optional, List
from sqlalchemy.orm import sessionmaker, Session, relationship

class PostService:
    """Post service with business logic"""

    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_all_posts(self, db_session: Session, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all posts with business logic"""
        posts = self.post_repo.get_all(db_session, limit)
        return [post.to_dict() for post in posts]

    def create_post(self, title: str, content: str, author_id: int, db_session: Session) -> Dict[str, Any]:
        """Create post with business validation"""
        # Validate author exists
        author = self.user_repo.get_by_id(author_id, db_session)
        if not author:
            raise ValueError("Author not found")

        # Basic validation
        if len(title) < 5:
            raise ValueError("Title too short")
        if len(content) < 10:
            raise ValueError("Content too short")

        post = self.post_repo.create(title, content, author_id, db_session)
        return post.to_dict()