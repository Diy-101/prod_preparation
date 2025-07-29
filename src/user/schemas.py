from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Annotated

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr