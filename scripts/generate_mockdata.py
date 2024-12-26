# type: ignore
from faker import Faker
import random
import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

fake = Faker()

# User -> Property -> Building -> Unit -> Lease -> Tenant -> Insurance

count_per_table = 50
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

user0 = {
    'id': 1,
    'name': 'Dan Hart',
    'email': 'dnstock8@gmail.com',
    'password': password_dan
}

property0 = {
    'id': 1,
    'name': 'The Jefferson',
    'address': '2 Kinderkamack Rd',
    'city': 'Hackensack',
    'state': 'NJ',
    'zip_code': '07601',
    'type': 'Commercial',
    'manager_id': 1
}

# Generate Users
def generate_users(count=count_per_table):
    global total_generated
    global user_ids
    users = []
    for i in range(count):
        if i == 0:
            user = user0
        else:
            user = {
                'id': i + 1,
                'name': fake.name(),
                'email': f'user{i+1}@example.com',
                'password': password_dan
            }
        users.append(user)
        user_ids.append(user['id'])
    total_generated += count
    return users

# Generate Properties (FK -> User)
def generate_properties(count=count_per_table):
    global total_generated
    global property_ids
    properties = []
    for i in range(count):
        if i == 0:
            property_ = property0
        else:
            property_ = {
                'id': i + 1,
                'name': fake.company(),
                'address': fake.address().replace('\n', ', '),
                'city': fake.city(),
                'state': fake.state_abbr(),
                'zip_code': fake.zipcode(),
                'type': random.choice(['Commercial', 'Residential']),
                'manager_id': random.choice(user_ids)
            }
        properties.append(property_)
        property_ids.append(property_['id'])
    total_generated += count
    return properties

# Generate Buildings (FK -> Property)
def generate_buildings(count=count_per_table):
    global total_generated
    global building_ids
    buildings = []
    for i in range(count):
        building = {
            'id': i + 1,
            'name': fake.company(),
            'unit_count': random.randint(50, 500),
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
def generate_units(count=count_per_table):
    global total_generated
    global unit_ids
    units = []
    for i in range(count):
        unit = {
            'id': i + 1,
            'unit_number': random.randint(100, 999),
            'floor_number': random.randint(1, 20),
            'bedrooms': random.randint(1, 5),
            'bathrooms': random.choice([1.0, 1.5, 2.0, 2.5, 3.0]),
            'sqft': random.randint(500, 2000),
            'is_vacant': random.choice([True, False]),
            'building_id': random.choice(building_ids),
        }
        units.append(unit)
        unit_ids.append(unit['id'])
    total_generated += count
    return units

# Generate Leases (FK -> Unit)
def generate_leases(count=count_per_table):
    global total_generated
    global lease_ids
    leases = []
    for i in range(count):
        start = fake.date_between(start_date='-1y', end_date='today')
        end = start + relativedelta(years=1)
        lease = {
            'id': i + 1,
            'start_date': start,
            'end_date': end,
            'rent': random.randint(1000, 5000),
            'unit_id': random.choice(unit_ids)
        }
        leases.append(lease)
        lease_ids.append(lease['id'])
    total_generated += count
    return leases

# Generate Tenants (FK -> Lease)
def generate_tenants(count=count_per_table):
    global total_generated
    global tenant_ids
    tenants = []
    for i in range(count):
        tenant = {
            'id': i + 1,
            'name': fake.name(),
            'email': f'tenant{i+1}@example.com',
            'phone': fake.phone_number(),
            'lease_id': random.choice(lease_ids)
        }
        tenants.append(tenant)
        tenant_ids.append(tenant['id'])
    total_generated += count
    return tenants

# Generate Insurances (FK -> Tenant)
def generate_insurances(count=count_per_table):
    global total_generated
    global insurance_ids
    insurances = []
    for i in range(count):
        insurance = {
            'id': i + 1,
            'policy_number': fake.uuid4(),
            'expiration_date': fake.date_this_decade(),
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
suffix = int(datetime.now().strftime('%Y%m%d'))
filename = f'mockdata_{suffix}.json'
with open(filename, 'w') as f:
    json.dump(mock_data, f, indent=4, default=custom_serializer)

print('Mock data generated successfully!')
print(f'Mocked {count_per_table} records in {len(mock_data)} tables.')
print(f'Total records generated: {total_generated}')
print(f'Filename: {filename}')
