# =========================
## APPLICATION
# =========================

# run application
uvicorn app.main:app --reload

# run tests
pytest tests/somefile.py

# =========================
## VIRTUAL ENVIRONMENT
# =========================

# create virtaul env
python3 -m venv venv

# activate virtaul env
source venv/bin/activate

# =========================
## DEPENDENCIES
# =========================

# generate dependency file
pip freeze > requirements.txt

# install dependencies
pip install -r requirements.txt

# =========================
## DATABASE MIGRATIONS
# =========================

# initialize db migrations
alembic init alembic

# generate new migration
alembic revision --autogenerate -m "Describe your changes"

# apply the migration
alembic upgrade head

# =========================
## POSTGRES
# =========================

# start postgresql
brew services start postgresql

# cli access
psql postgres

