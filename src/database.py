from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from src.constants import DB_URL

engine = create_engine(DB_URL)

metadata = MetaData()
metadata.reflect(bind=engine)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass