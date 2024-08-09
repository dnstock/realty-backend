#
# Generate a new database migration.
#
# Usage:
#   ./migrate.sh "Describe your changes"

if [ $# -gt 1 ]; then
  echo "Too many arguments.\n"
elif [ -n "$1" ]; then
  alembic revision --autogenerate -m "$1"
else
  echo "Cannot have empty message.\n"
fi
