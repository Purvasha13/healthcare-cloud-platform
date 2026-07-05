from fastapi import FastAPI
from app.database import check_database_connection 
app = FastAPI(
    title="Secure Healthcare Cloud Platform",
    description="Production-style Healthcare Cloud Platform built using FastAPI.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Secure Healthcare Cloud Platform"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Secure Healthcare Cloud Platform"
    }


@app.get("/version")
def version():
    return {
        "version": "0.1.0",
        "environment": "development"
    }

@app.get("/db-health")
def database_health():
    return check_database_connection()