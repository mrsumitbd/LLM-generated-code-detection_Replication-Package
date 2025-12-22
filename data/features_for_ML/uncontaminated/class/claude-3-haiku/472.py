from typing import Callable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DatabaseConfig

class DatabaseEngine:
    """SQLAlchemy engine service (singleton)"""

    def __init__(self, config: DatabaseConfig = Depends("database_config")):
        self.config = config
        self.engine = create_engine(self.config.database_url)
        self.Session = sessionmaker(bind=self.engine)

    def _seed_benchmark_data(self):
        # Implement the logic to seed benchmark data
        pass

    def get_session(self) -> Callable[[], None]:
        """
        Returns a context manager that provides a SQLAlchemy session.
        """
        return self.Session