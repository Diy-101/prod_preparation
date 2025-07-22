from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
from os import getenv

load_dotenv("../.env")

user = getenv("DB_USER")
password = getenv("DB_PASS")
host = getenv("DB_HOST")
port = getenv("DB_PORT")
name = getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}")

metadata = MetaData()
metadata.reflect(bind=engine)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass