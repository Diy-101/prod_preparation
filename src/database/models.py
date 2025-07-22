from src.database.connection import metadata
from src.database.connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    alpha2 = Column(String(2), nullable=False)
    alpha3 = Column(String(3), nullable=False)
    region = Column(String(100))

