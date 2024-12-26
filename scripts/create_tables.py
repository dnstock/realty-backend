# USAGE NOTE:
#   Run this script with the command `./scripts/create_tables` from the root directory

'''
This does not handle database migrations, and therefore
going through Alembic is recommended for production use.
'''

import sys
from sqlalchemy import create_engine
from db import Base

if len(sys.argv) != 2:
    print("Error: Missing database name")
    sys.exit(1)

database = sys.argv[1]
engine = create_engine(f'postgresql+psycopg://admin:admin@localhost/{database}')

print(f'Creating tables in database: {database}')

# Base.metadata.drop_all(bind=engine) # Uncomment to drop all tables first
Base.metadata.create_all(bind=engine)

print('Tables created successfully!')
