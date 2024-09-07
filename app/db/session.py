from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from typing import Generator
from core import settings

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

# Dependency to get the DB session
def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()

# Return the session directly
def get_db_session() -> Session:
    return next(get_db()) # Advance the generator to get the session
