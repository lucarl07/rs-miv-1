# Starts local environment
source .venv/bin/activate

# Run API with Uvicorn
uvicorn app.main:app --reload
