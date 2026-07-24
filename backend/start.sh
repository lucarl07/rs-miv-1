# Migrate database
alembic upgrade head

# Run API with Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port $PORT
