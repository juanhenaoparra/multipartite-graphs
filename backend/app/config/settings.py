# app/settings.py
from starlette.config import Config
from starlette.datastructures import Secret
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

config = Config(os.getcwd()+"/app/config/.env")

PROJECT_NAME = "Backend anal"
PROJECT_VERSION = "1.0.0"

DEBUG = config("DEBUG", cast=bool, default=False)

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
Base = declarative_base()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


print("database connected successfully!")

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()