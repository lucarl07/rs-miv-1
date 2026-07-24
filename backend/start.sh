# Set default values
HOST=0.0.0.0
PORT=8000

# Migrate database
alembic upgrade head

# Run API with Uvicorn
uvicorn app.main:app --host $HOST --port $PORT
