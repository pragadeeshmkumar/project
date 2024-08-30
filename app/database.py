from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = " "

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker( bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
