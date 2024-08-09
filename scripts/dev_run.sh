#
# Run application server in development environment.
#

export ENVIRONMENT=development
uvicorn app.main:app --reload
