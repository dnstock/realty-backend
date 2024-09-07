# Realty Project

This is a full-stack application for property management, combining a FastAPI backend and a React frontend.

## Project Structure

```
realty/
│
├── backend/ # Backend code (FastAPI, database models, migrations)
├── frontend/ # Frontend code (React, components, services)
├── docker-compose.yml # Docker setup for both frontend and backend
└── README.md # Project documentation
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Node.js and npm installed if running frontend locally outside of Docker.

### Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/realty.git
    cd realty
    ```

1. **Set up environment variables:**
   - Create `.env` file and fill in appropriate values. Refer to `backend/envs/.env.example` file.
   - Optionally, create environment-specific files. Refer to `backend/envs/*.example` files.

1. **Set up database and run migrations:**
    - Create a PostgreSQL database.
    - Create a user with r+w access to the database.

1. **Run migrations to initialize database:**
    ```bash
    export ENVIRONMENT=development
    alembic upgrade head
    ```

1. **Run unit tests for the application:**
    ```bash
    pytest tests
    ```

1. **Setup Docker to use development environment:**
    ```bash
    # Copy the docker-compose-env file to .env
    cp docker-compose-env .env

    # Open .env and uncomment the development mode section
    vi .env
    ```

1. **Run the application with Docker:**
    ```bash
    docker-compose up --build
    ```

1. **Access the application:**
   - Backend API: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

### Useful Commands

- **Start the services:**
    ```bash
    docker compose up --build
    ```

- **Stop the services:**
    ```bash
    docker compose down
    ```

- **Rebuild the services:**
    ```bash
    docker compose up --build
    ```

### Project Details

- **Backend:** FastAPI, PostgreSQL
- **Frontend:** React, Axios, React Router

## License

This application contains proprietary code and may not be used, copied or distributed.
