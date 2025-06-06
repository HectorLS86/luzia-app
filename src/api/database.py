from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Sustituye esta URL por la que copiaste de Railway (DATABASE_URL)
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@host:port/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
