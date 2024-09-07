from sqlalchemy.orm import Session
from db import Base, engine

# Create tables if they don't exist
def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
    # Optionally, load seed data here
    # Example:
    # user = models.User(email="admin@example.com", is_superuser=True)
    # db.add(user)
    # db.commit()
