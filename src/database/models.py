from src.database.connection import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    alpha_2 = Column(String(2), index=True, nullable=False)
    alpha_3 = Column(String(3), index=True, nullable=False)
    region = Column(String, index=True)