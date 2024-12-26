# USAGE NOTE:
#   Run this script with the command `./scripts/load_mockdata` from the root directory

import sys
import json
from pathlib import Path
from typing import Any
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from db.models import User, Property, Building, Unit, Tenant, Lease, Insurance

# Create database connection
def connect_to_database(target_database_name: str) -> Session:
    engine = create_engine(f'postgresql+psycopg://admin:admin@localhost:5432/{target_database_name}')
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session()

# Parse mock data from JSON file
def read_from_file(mockdata_filename: str) -> dict[str, Any]:
    file = Path(mockdata_filename)
    print(f'Reading mock data from: {file}')

    try:
        with open(file) as f:
            return json.load(f)
    except (FileNotFoundError, PermissionError) as e:
        print(f'Error reading {file}: {e}')
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f'Error parsing {file}: {e}')
        sys.exit(1)

# Load mock data into the database
def load_mockdata(data: dict[str, Any], session: Session) -> None:
    print(f'Loading mock data into the database...')
    total_loaded:int = 0
    try:
        # Load Users
        for user_data in data["users"]:
            user = User(**user_data)  # Assumes User ORM accepts fields as kwargs
            session.add(user)
        total_loaded += len(data["users"])
        print(f'Loaded {len(data["users"])} user records. Total loaded: {total_loaded}')

        # Load Properties
        for property_data in data["properties"]:
            property_ = Property(**property_data)
            session.add(property_)
        total_loaded += len(data["properties"])
        print(f'Loaded {len(data["properties"])} property records. Total loaded: {total_loaded}')

        # Load Buildings
        for building_data in data["buildings"]:
            building = Building(**building_data)
            session.add(building)
        total_loaded += len(data["buildings"])
        print(f'Loaded {len(data["buildings"])} building records. Total loaded: {total_loaded}')

        # Load Units
        for unit_data in data["units"]:
            unit = Unit(**unit_data)
            session.add(unit)
        total_loaded += len(data["units"])
        print(f'Loaded {len(data["units"])} unit records. Total loaded: {total_loaded}')

        # Load Tenants
        for tenant_data in data["tenants"]:
            tenant = Tenant(**tenant_data)
            session.add(tenant)
        total_loaded += len(data["tenants"])
        print(f'Loaded {len(data["tenants"])} tenant records. Total loaded: {total_loaded}')

        # Load Leases
        for lease_data in data["leases"]:
            lease = Lease(**lease_data)
            session.add(lease)
        total_loaded += len(data["leases"])
        print(f'Loaded {len(data["leases"])} lease records. Total loaded: {total_loaded}')

        # Load Insurances
        for insurance_data in data["insurances"]:
            insurance = Insurance(**insurance_data)
            session.add(insurance)
        total_loaded += len(data["insurances"])
        print(f'Loaded {len(data["insurances"])} insurance records. Total loaded: {total_loaded}')

        # Commit all transactions
        session.commit()
        print("Mock data successfully loaded into the database.")
        print(f'Total records loaded: {total_loaded} across {len(data)} tables.')

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
        print(f'Rolled back transactions for {total_loaded} records.')

    finally:
        session.close()

def main():
    # Check args
    if len(sys.argv) != 3:
        print("Error: Missing parameters for mock data filename and/or target database name.")
        sys.exit(1)

    target_database_name = sys.argv[1]
    mockdata_filename = sys.argv[2]

    load_mockdata(
        read_from_file(mockdata_filename),
        connect_to_database(target_database_name)
    )
    print('Process complete.')

if __name__ == "__main__":
    main()
