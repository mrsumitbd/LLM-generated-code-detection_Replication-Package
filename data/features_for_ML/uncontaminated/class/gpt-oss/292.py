from typing import List, Dict, Any
from sqlalchemy.orm import Session

class PostService:
    """Post service with business logic"""

    def __init__(self, post_repo, user_repo):
        """
        Initialize the service with repositories.

        :param post_repo: Repository handling Post persistence.
        :param user_repo: Repository handling User persistence.
        """
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_all_posts(self, db_session: Session, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all posts up to the specified limit.

        :param db_session: SQLAlchemy session for DB operations.
        :param limit: Maximum number of posts to return.
        :return: List of posts represented as dictionaries.
        """
        posts = self.post_repo.get_all(db_session, limit=limit)
        return [self._post_to_dict(p) for p in posts]

    def create_post(self, title: str, content: str, author_id: int, db_session: Session) -> Dict[str, Any]:
        """
        Create a new post after validating the author exists.

        :param title: Title of the post.
        :param content: Content of the post.
        :param author_id: ID of the author.
        :param db_session: SQLAlchemy session for DB operations.
        :return: The created post represented as a dictionary.
        :raises ValueError: If the author does not exist.
        """
        author = self.user_repo.get_by_id(db_session, author_id)
        if not author:
            raise ValueError(f"Author with id {author_id} does not exist")

        post = self.post_repo.create(db_session, title=title, content=content, author_id=author_id)
        return self._post_to_dict(post)

    @staticmethod
    def _post_to_dict(post) -> Dict[str, Any]:
        """
        Convert a Post ORM object to a plain dictionary.

        :param post: Post ORM instance.
        :return: Dictionary representation of the post.
        """
        # Assuming the Post model has __dict__ that contains all columns.
        # Exclude SQLAlchemy internal attributes if present.
        data = {k: v for k, v in post.__dict__.items() if not k.startswith('_sa_')}
        return data