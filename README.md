# Realty.AI Backend

Backend API service for real estate property management platform.

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

- Python 3.x
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
- Python 3.x
- PostgreSQL
- Redis
- Docker (optional)

### Installation

1. Clone the repository
2. Create a virtual environment:
```sh
python3 -m venv venv source venv/bin/activate
```
3. Install dependencies:
```sh
pip install -r requirements.txt
```
4. Copy environment file:
```sh
cp .env.example .env
```
5. Configure environment variables in the `.env` file.

### Running Locally

Start the development server:

```sh
uvicorn app.main:app --reload
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

### Database Migrations

Create a new migration:
```sh
alembic revision --autogenerate -m "Description"
```

Apply migrations:
```sh
alembic upgrade head
```

### Running Tests

Execute the test suite:

```sh
pytest
```

## API Documentation

Once running, view the interactive API documentation at:
- Swagger UI:
    ```
    http://localhost:8000/docs
    ```

- ReDoc:
    ```
    http://localhost:8000/redoc
    ```

## Environment Variables Key environment variables for configuration:
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

See  the `.env.example` file for all available configuration options.

## Project Structure
```
.
├── alembic/            # Database migrations
├── app/
│ ├── api/              # API endpoints and routing
│ ├── controllers/      # Business logic
│ ├── core/             # Core functionality
│ ├── db/               # Database models and config
│ ├── schemas/          # Pydantic models
│ └── tests/            # Test suite
├── envs/               # Environment settings
├── logs/               # App log files
└── scripts/            # Utility scripts
```

## License

Private and Confidential. All rights reserved.
