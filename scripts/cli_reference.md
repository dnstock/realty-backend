```bash
# =========================
## DOCKER
# =========================

# start the app
docker-compose up

# stop the app
docker-compose down

# rebuild the app
docker-compose up --build

# (from backend dir) build the image with a different environment
docker build --build-arg ENVIRONMENT=production -t realty-backend .

# (from backend dir) run the container with a different environment
docker run -e ENVIRONMENT=production -p 8000:8000 realty-backend

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
```
