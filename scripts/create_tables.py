'''
Creates database tables as defined in the `models.py` file.
This does not handle database migrations, and therefore
should likely never be used. Instead use Alembic.

Usage:
    python create_tables.py
'''

from sqlalchemy import create_engine
from app.models import Base
from app.config import settings

# Create the engine using the database URL
engine = create_engine(settings.DATABASE_URL)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
