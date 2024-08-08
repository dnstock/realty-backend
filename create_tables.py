from sqlalchemy import create_engine
from app.models import Base
from app.config import settings

# Create the engine using the database URL
engine = create_engine(settings.DATABASE_URL)

# Create all tables in the database
Base.metadata.create_all(bind=engine)
