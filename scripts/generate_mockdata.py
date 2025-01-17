# type: ignore
from faker import Faker
import random
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance

# True = Start IDs as defined below
# False = Start all IDs at 1 (ignores below)
USE_ID_STARTS = False

# Start IDs for each table (if appending to existing data)
user_id_start = 51
property_id_start = 51
building_id_start = 51
unit_id_start = 51
lease_id_start = 51
tenant_id_start = 51
insurance_id_start = 51

# Number of records to generate for each table
users_per_table = random.randint(10, 30)
properties_per_table = random.randint(50, 100)
buildings_per_table = random.randint(500, 1000)
units_per_table = random.randint(3000, 8000)
leases_per_table = random.randint(3000, 8000)
tenants_per_table = random.randint(3000, 8000)
insurances_per_table = random.randint(3000, 8000)


""" NO CHANGES NEEDED BELOW THIS LINE """

fake = Faker()

suffix = input('Enter a suffix for the filename (default: YYYYMMDD): ')
suffix = suffix if suffix else datetime.now().strftime('%Y%m%d')
filename = f'mockdata_{suffix}.json'

total_generated = 0

# Storage for foreign key relationships
user_ids = []
property_ids = []
building_ids = []
unit_ids = []
lease_ids = []
tenant_ids = []
insurance_ids = []

# this encrypted password = 'dan'
password_dan = '$2b$12$h7Vc0GuUPiSDQ5CoGX7e4Okro4ZYM/LZPXsVo./4uUhG.SybOHG.6'

user1 = {
    'id': 1,
    'name': 'Dan Hart',
    'email': 'dnstock8@gmail.com',
    'password': password_dan,
}

property1 = {
    'id': 1,
    'name': 'The Jefferson',
    'address': '2 Kinderkamack Rd',
    'city': 'Hackensack',
    'state': 'NJ',
    'zip_code': '07601',
    'type': 'Commercial',
    'manager': 'Dan Hart',
    'owner_id': 1,
}

def _generate_metadata(id):
    return {
        'id': id,
        'owner_id': 1,  # me
        'is_active': True if random.random() < 0.9 else False,  # ~10% are inactive
        'is_flagged': True if random.random() < 0.1 else False,  # ~10% are flagged
        'notes': fake.text() if random.random() < 0.3 else None,  # ~30% have notes
    }

# Generate Users
def generate_users(count=users_per_table):
    global total_generated
    global user_ids
    users = []
    for i in range(count):
        id = user_id_start + i if USE_ID_STARTS else i + 1
        if id == 1:
            user = user1
        else:
            user = {
                'id': id,
                'name': fake.name(),
                'email': f'user{id}@example.com',
                'password': password_dan,
                'is_active': True if random.random() < 0.6 else False, # ~40% are inactive
                'is_flagged': True if random.random() < 0.2 else False, # ~20% are flagged
                'notes': fake.text() if random.random() < 0.3 else None,  # ~30% have notes
            }
        users.append(user)
        user_ids.append(user['id'])
    total_generated += count
    return users

# Generate Properties
def generate_properties(count=properties_per_table):
    global total_generated
    global property_ids
    properties = []
    for i in range(count):
        id = property_id_start + i if USE_ID_STARTS else i + 1
        if id == 1:
            property_ = property1
        else:
            property_ = {
                **_generate_metadata(id),
                'name': fake.company(),
                'address': fake.address().replace('\n', ', '),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip_code': fake.zipcode(),
                'type': random.choice(['Commercial', 'Residential']),
                'manager': fake.name(),
            }
        properties.append(property_)
        property_ids.append(property_['id'])
    total_generated += count
    return properties

# Generate Buildings (FK -> Property)
def generate_buildings(count=buildings_per_table):
    global total_generated
    global building_ids
    buildings = []
    for i in range(count):
        id = building_id_start + i if USE_ID_STARTS else i + 1
        building = {
            **_generate_metadata(id),
            'name': fake.company(),
            'floor_count': random.randint(3, 20),
            'has_elevator': random.choice([True, False]),
            'has_pool': random.choice([True, False]),
            'has_gym': random.choice([True, False]),
            'has_parking': random.choice([True, False]),
            'has_doorman': random.choice([True, False]),
            'property_id': random.choice(property_ids),
        }
        buildings.append(building)
        building_ids.append(building['id'])
    total_generated += count
    return buildings

# Generate Units (FK -> Building)
def generate_units(count=units_per_table):
    global total_generated
    global unit_ids
    units = []
    for i in range(count):
        id = unit_id_start + i if USE_ID_STARTS else i + 1
        unit = {
            **_generate_metadata(id),
            'unit_number': random.randint(100, 999),
            'floor_number': random.randint(1, 20),
            'bedrooms': random.randint(1, 5),
            'bathrooms': random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
            'sqft': random.randint(500, 2000),
            'is_vacant': True if random.random() < 0.4 else False,  # ~60% are occupied
            'building_id': random.choice(building_ids),
        }
        units.append(unit)
        unit_ids.append(unit['id'])
    total_generated += count
    return units

# Generate Leases (FK -> Unit)
def generate_leases(count=leases_per_table):
    global total_generated
    global lease_ids
    leases = []
    for i in range(count):
        id = lease_id_start + i if USE_ID_STARTS else i + 1
        start = fake.date_between(start_date='-540d', end_date='today')  # Have some expired leases
        end = start + relativedelta(years=1)  # 1-year lease
        lease = {
            **_generate_metadata(id),
            'start_date': start,
            'end_date': end,
            'rent': random.randint(1000, 5000),
            'deposit': random.randint(1000, 5000),
            'unit_id': random.choice(unit_ids)
        }
        leases.append(lease)
        lease_ids.append(lease['id'])
    total_generated += count
    return leases

# Generate Tenants (FK -> Lease)
def generate_tenants(count=tenants_per_table):
    global total_generated
    global tenant_ids
    tenants = []
    for i in range(count):
        id = tenant_id_start + i if USE_ID_STARTS else i + 1
        tenant = {
            **_generate_metadata(id),
            'name': fake.name(),
            'email': f'tenant{id}@example.com',
            'phone': fake.phone_number(),
            'lease_id': random.choice(lease_ids)
        }
        tenants.append(tenant)
        tenant_ids.append(tenant['id'])
    total_generated += count
    return tenants

# Generate Insurances (FK -> Tenant)
def generate_insurances(count=insurances_per_table):
    global total_generated
    global insurance_ids
    insurances = []
    for i in range(count):
        id = insurance_id_start + i if USE_ID_STARTS else i + 1
        effective = fake.date_this_decade()  # Random effective date
        expiration = effective + relativedelta(years=3)  # 3-year policy
        insurance = {
            **_generate_metadata(id),
            'provider': fake.company(),
            'policy_type': random.choice(['Renters', 'Homeowners', 'Condo']),
            'policy_number': fake.uuid4(),
            'premium': random.randint(100, 500),
            'effective_date': effective,
            'expiration_date': expiration,
            'tenant_id': random.choice(tenant_ids)
        }
        insurances.append(insurance)
        insurance_ids.append(insurance['policy_number'])
    total_generated += count
    return insurances

# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance

# Generate all mock data
def generate_mock_data():
    global total_generated
    data = {
        'users': generate_users(),
        'properties': generate_properties(),
        'buildings': generate_buildings(),
        'units': generate_units(),
        'leases': generate_leases(),
        'tenants': generate_tenants(),
        'insurances': generate_insurances()
    }
    return data

# Custom function to handle non-serializable objects
def custom_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()  # Convert `date` to ISO 8601 string
    raise TypeError(f"Type {type(obj)} not serializable")

# Save to JSON
mock_data = generate_mock_data()
with open(filename, 'w') as f:
    json.dump(mock_data, f, indent=4, default=custom_serializer)

print('=' * 50)
print('Data generated successfully!'.center(50))
print('=' * 50)
print(f'Mocked {total_generated} records in {len(mock_data)} tables.')
print('-' * 50)
print(f'Users: {users_per_table}')
print(f'Properties: {properties_per_table}')
print(f'Buildings: {buildings_per_table}')
print(f'Units: {units_per_table}')
print(f'Leases: {leases_per_table}')
print(f'Tenants: {tenants_per_table}')
print(f'Insurances: {insurances_per_table}')
print('=' * 50)
print(f'Filename: {filename}')
print('=' * 50)
