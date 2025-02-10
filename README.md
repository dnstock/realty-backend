# Realty Backend

## Description

Backend API Service for the real estate management system. This application is part of the Realty platform. It works in conjunction with the [Frontend User Interface](https://github.com/dnstock/realty-frontend) to provide a complete solution for managing commercial real estate properties.

## Features

- RESTful API endpoints for managing properties, buildings, units, leases and tenants
- JWT authentication and authorization
- Role-based access control
- Database migrations with Alembic
- Logging with configurable outputs
- Docker support for development and production
- Comprehensive test suite
- CORS configuration
- Request ID tracking
- Configurable alerts (email, SMS, Slack)
- More...

## Tech Stack

- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- Docker
- Pytest
- More...

## Getting Started

### Prerequisites
- Python 3.13+
- PostgreSQL
- Redis
- Docker (optional)

### Frontend User Interface

The frontend UI is a separate application that works in conjunction with the backend API. It is available at: [https://github.com/dnstock/realty-frontend](https://github.com/dnstock/realty-frontend)

### Installation

This app uses [Poetry](https://python-poetry.org/) for dependency management. Install it first if you don't have it already:
```sh
curl -sSL https://install.python-poetry.org | python3 -
# or
pip install poetry
```

Clone the repository:
```sh
git clone git@github.com:dnstock/realty-backend.git
cd realty-backend
```

Install dependencies:
```sh
poetry install
```

Activate the virtual environment:
```sh
poetry shell
# or
source $(poetry env info --path)/bin/activate
```

### Database Setup

Create a PostgreSQL database:
```sh
createdb realty
```

Apply the initial database schema:
```sh
alembic upgrade head
# or
./scripts/dev_migrate
```

### Configuration

Create a `.env` file from the template:
```sh
cp envs/.env_template envs/.env
```

Edit the `.env` file and configure the environment variables.
```sh
vim envs/.env
```

## Running Locally

Start the development server:

```sh
uvicorn app.main:app --reload
# or
./scripts/dev_run
```

The API will be available at:

    http://localhost:8000

### Docker Setup

Build and run with Docker Compose:
```sh
docker-compose up --build
```

For production:
```sh
docker-compose -f docker-compose.prod.yml up -d
```

## Database Migrations

Create a new migration:
```sh
alembic revision --autogenerate -m "Description"
# or
./scripts/migrate "Description"
```

Apply migrations:
```sh
alembic upgrade head
# or
./scripts/dev_migrate
```

## Running Tests

Execute the test suite:

```sh
pytest
```

To run a specific test file:
```sh
pytest app/tests/test_example.py
# or
./scripts/test example
```

To run a specific test case:
```sh
pytest app/tests/test_example.py::test_example
# or
./scripts/test example test_example
```

Usage of the `scripts/test` script:
```sh
./scripts/test <test_file> [test_case]
```

## Linting and Formatting

Run the linter:
```sh
flake8
```

Format the code:
```sh
black .
```

## Logging

View the log files in the `logs` directory:
```sh
tail -f logs/app.log
```

The log level can be configured in the `.env` file:
```ini
LOG_LEVEL=debug
```

The log format can also be configured:
```ini
LOG_FORMAT=json
```

Other logging configuration options are available in the `.env` file.

## API Documentation

Once running, view and test the API with Swagger:
```
http://localhost:8000/docs
```

ReDoc can also be used for a more structured view:
```sh
http://localhost:8000/redoc
```

## Authentication

The API uses JWT for authentication. Obtain a token by sending a POST request to the `/auth/login` endpoint with the following payload:
```json
{
    "username": "admin",
    "password": "password"
}
```

Use the token in the `Authorization` header for subsequent requests:
```json
{
    "Authorization": "Bearer <token>"
}
```

## Authorization

The API uses role-based access control. The available roles are:

- `admin`
- `manager`
- `staff`
- `tenant`

The `admin` role has full access to all resources. The other roles have specific permissions based on the resource.

## CORS Configuration

The API has CORS enabled by default. The allowed origins can be configured in the `.env` file:
```ini
API_CORS_ORIGINS=["http://localhost:3000"]
```

## Request ID Tracking

Each request is assigned a unique ID that is included in the response headers. This can be used for tracking and debugging purposes.

Log messages are also tagged with the request ID for easier correlation.

## Alerts

The API can be configured to send alerts via email, SMS or Slack. The alert settings can be configured in the `.env` file:
```ini
ALERT_EMAIL_ENABLED=true
ALERT_SMS_ENABLED=false
ALERT_SLACK_ENABLED=false
```

## Utility Scripts

The `scripts` directory contains utility scripts for common tasks:

- `dev_run`: Start the development server
- `dev_migrate`: Apply database migrations
- `migrate`: Create a new database migration
- `test`: Run specific tests or test files
- `activate`: Print the virtual environment activation command
- `clear_cache`: Clear the LRU cache
- `generate_secret_key`: Generate a new secret key (for JWT)

## Environment Variables

Sample environment variables in configuration template:

```ini
# Application
APP_NAME=realty-api
APP_ENV=development
APP_DEBUG=true

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=realty

# Authentication
JWT_SECRET_KEY=secret
JWT_ALGORITHM=HS256

# Logging
LOG_LEVEL=debug
LOG_FORMAT=json
```

See the `envs/.env_template` file for all available configuration options.

## Project Structure
```
.
├── alembic/                    # Database migrations
│   └── versions/               # Migration scripts
├── app/
│   ├── api/                    # API routes and core logic
│   │   └── v1/                 # API version 1
│   │       └── endpoints/      # API endpoints
│   ├── controllers/            # Business logic
│   ├── core/                   # Core functionality
│   ├── db/                     # Database core logic
│   │   └── models/             # SQLAlchemy models
│   ├── schemas/                # Pydantic models
│   │   └── utils/              # Schema utilities
│   └── tests/                  # Test suite
├── envs/                       # Environment settings
├── logs/                       # App log files
├── scripts/                    # Utility scripts
├── pyproject.toml              # Poetry configuration
└── README.md                   # Project README
```

## License

Private and Confidential. All rights reserved.
