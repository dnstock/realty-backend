from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from core import settings
import contextvars

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

# Create a context variable to hold the db session
db_context: contextvars.ContextVar[Session | None] = contextvars.ContextVar("db_session", default=None)

def get_db() -> Session:
    db = db_context.get()
    if db is None:
        raise Exception("Database session not found")
    return db
