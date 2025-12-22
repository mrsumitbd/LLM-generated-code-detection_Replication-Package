from typing import List, Dict, Any
from sqlalchemy.orm import Session
from post_repository import PostRepository
from user_repository import UserRepository

class PostService:
    """Post service with business logic"""

    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_all_posts(self, db_session: Session, limit: int = 100) -> List[Dict[str, Any]]:
        return self.post_repo.get_all_posts(db_session, limit)

    def create_post(self, title: str, content: str, author_id: int, db_session: Session) -> Dict[str, Any]:
        author = self.user_repo.get_user_by_id(db_session, author_id)
        if author is None:
            raise ValueError("Author with id {} not found".format(author_id))
        
        post_data = {
            'title': title,
            'content': content,
            'author_id': author_id
        }
        return self.post_repo.create_post(db_session, post_data)