from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://palcode_dev:palcode123!#%@91.108.110.211:5433/blog_platform"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker( bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()