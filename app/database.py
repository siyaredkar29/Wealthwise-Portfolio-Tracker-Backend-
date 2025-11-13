import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") #fetches the db connection string from .env
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set. Create .env from .env.example.")

engine = create_engine(DATABASE_URL, echo=False, future=True) #creates the database engine
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
