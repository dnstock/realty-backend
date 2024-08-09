#
# Execute database migrations in development environment.
#

export ENVIRONMENT=development
alembic upgrade head
