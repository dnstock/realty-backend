from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from core import settings
from contextvars import ContextVar
from typing import Optional

# Create a context variable to hold the db session
db_session_context: ContextVar[Optional[Session]] = ContextVar("db_session", default=None)

engine = create_engine(
    settings.postgres_url,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    future=settings.sqlalchemy_future,
    echo=settings.sqlalchemy_echo,
    pool_pre_ping=True,  # Ensure that connections are alive
)

# Ensure thread-safe sessions (each request gets its own session)
SessionLocal = scoped_session(sessionmaker(
    autocommit=False, 
    autoflush=False,
    bind=engine
))

def get_db() -> Session:
    db = db_session_context.get()
    if db is None:
        raise Exception("Database session not found")
    return db
