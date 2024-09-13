from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def initialize_db(postgres_host: str, postgres_db_name: str, postgres_port: int, postgres_username: str, postgres_password: str):
    DATABASE_URL = f"postgresql://{postgres_username}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db_name}"
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

session_local = initialize_db(POSTGRES_HOST, POSTGRES_DB_NAME, POSTGRES_PORT, POSTGRES_USERNAME, POSTGRES_PASSWORD)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
