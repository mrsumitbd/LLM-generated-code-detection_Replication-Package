class PostService:
    """Post service with business logic"""

    def __init__(self, post_repo: PostRepository, user_repo: UserRepository):
        self.post_repo = post_repo
        self.user_repo = user_repo

    def get_all_posts(self, db_session: Session, limit: int = 100) -> List[Dict[str, Any]]:
        posts = self.post_repo.get_all(db_session, limit)
        return [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author_id": post.author_id,
                "created_at": post.created_at,
                "updated_at": post.updated_at,
            }
            for post in posts
        ]

    def create_post(self, title: str, content: str, author_id: int, db_session: Session) -> Dict[str, Any]:
        user = self.user_repo.get_by_id(db_session, author_id)
        if not user:
            raise ValueError(f"User with id {author_id} not found")
        
        post = self.post_repo.create(
            db_session,
            title=title,
            content=content,
            author_id=author_id,
        )
        
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at,
        }