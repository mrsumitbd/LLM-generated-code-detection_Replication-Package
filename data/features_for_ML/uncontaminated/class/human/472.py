from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.pool import StaticPool
from catzilla import Catzilla, service, Depends, JSONResponse, BaseModel, Path, Query

class DatabaseEngine:
    """SQLAlchemy engine service (singleton)"""

    def __init__(self, config: DatabaseConfig = Depends("database_config")):
        self.config = config

        # Create SQLAlchemy engine optimized for performance
        self.engine = create_engine(
            config.database_url,
            echo=config.echo,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False}
        )

        # Create all tables
        Base.metadata.create_all(self.engine)

        # Create session factory
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False
        )

        # Seed benchmark data
        self._seed_benchmark_data()

    def _seed_benchmark_data(self):
        """Seed data optimized for benchmarking"""
        session = self.SessionLocal()
        try:
            # Create 1000 users for realistic load testing
            users = []
            for i in range(1000):
                user = User(
                    name=f"User {i}",
                    email=f"user{i}@benchmark.com"
                )
                users.append(user)

            session.add_all(users)
            session.commit()

            # Create 5000 posts for realistic load testing
            posts = []
            for i in range(5000):
                post = Post(
                    title=f"Post Title {i}",
                    content=f"This is the content for post number {i}. " * 10,  # Realistic content size
                    author_id=(i % 1000) + 1  # Distribute posts among users
                )
                posts.append(post)

            session.add_all(posts)
            session.commit()

        finally:
            session.close()