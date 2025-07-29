from sqlalchemy import Column, Integer, String, Boolean
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    countryCode = Column(String(2))
    isPublic = Column(Boolean)
    phone = Column(String, unique=True, index=True)
    image = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)