from typing import List, Dict, Any
from sqlalchemy.orm import Session
from repositories.post_repository import PostRepository
from repositories.user_repository import UserRepository
from models.post import Post

class PostService:
    """Post service with business logic"""

    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_all_posts(self, db_session: Session, limit: int = 100) -> List[Dict[str, Any]]:
        posts = self.post_repo.get_all(db_session, limit=limit)
        return [post.to_dict() for post in posts]

    def create_post(self, title: str, content: str, author_id: int, db_session: Session) -> Dict[str, Any]:
        author = self.user_repo.get_by_id(db_session, author_id)
        if not author:
            raise ValueError("Invalid author ID")

        post = Post(title=title, content=content, author=author)
        db_session.add(post)
        db_session.commit()
        return post.to_dict()