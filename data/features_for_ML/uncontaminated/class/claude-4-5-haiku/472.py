from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

class DatabaseEngine:
    """SQLAlchemy engine service (singleton)"""
    
    _instance: Optional['DatabaseEngine'] = None
    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker] = None

    def __new__(cls, config: 'DatabaseConfig' = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: 'DatabaseConfig' = None):
        if self._engine is None and config is not None:
            self.config = config
            self._engine = create_engine(
                config.database_url,
                echo=config.echo,
                pool_size=config.pool_size,
                max_overflow=config.max_overflow,
                pool_pre_ping=config.pool_pre_ping
            )
            self._session_factory = sessionmaker(bind=self._engine)
            self._seed_benchmark_data()

    def _seed_benchmark_data(self):
        """Seed initial benchmark data into the database"""
        if self._session_factory is None:
            return
        
        session = self._session_factory()
        try:
            # Check if data already exists
            from sqlalchemy import text
            result = session.execute(text("SELECT COUNT(*) FROM sqlite_master WHERE type='table'"))
            if result.scalar() > 0:
                return
        except Exception:
            pass
        finally:
            session.close()

    @property
    def engine(self) -> Engine:
        """Get the SQLAlchemy engine"""
        if self._engine is None:
            raise RuntimeError("DatabaseEngine not initialized")
        return self._engine

    @contextmanager
    def get_session(self) -> Session:
        """Get a database session"""
        if self._session_factory is None:
            raise RuntimeError("DatabaseEngine not initialized")
        
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dispose(self):
        """Dispose of the engine and close all connections"""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
            self._session_factory = None