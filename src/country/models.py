from sqlalchemy import Column, Integer, String
from src.database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    alpha2 = Column(String(2), nullable=False, unique=True)
    alpha3 = Column(String(3), nullable=False, unique=True)
    region = Column(String(100))