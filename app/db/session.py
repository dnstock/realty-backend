from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core import settings
from typing import Generator

engine = create_engine(
    settings.postgres_url,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    future=settings.sqlalchemy_future,
    echo=settings.sqlalchemy_echo,
    pool_pre_ping=True,  # Ensure that connections are alive
)

# Create database session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create new database session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
