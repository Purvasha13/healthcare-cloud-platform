import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not configured. Please check your .env file."
    )