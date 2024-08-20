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
engine = create_engine(settings.database_url)

# Create all tables in the database
#(UNCOMMENT THE LINE BELOW BEFORE RUNNING THIS SCRIPT)
#Base.metadata.create_all(bind=engine)
