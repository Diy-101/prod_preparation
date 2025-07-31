from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
import jwt
import src.user.models as models
import src.user.schemas as schemas
from src.database import get_db

load_dotenv()

SECRET_KEY = getenv("AUTH_SECRET_KEY")
ALGORITHM = getenv("AUTH_ALGORITHM")
ACCESS_TOKEN_TIME_MINUTES = int(getenv("AUTH_TOKEN_TIME_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/sign-in")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_TIME_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload["sub"]
        if username is None:
            return None
        return username
    except jwt.PyJWTError:
        return None

async def get_profile_via_token(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    username = verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Переданный токен не существует либо некорректен.",
        )
    user = db.query(models.User).filter(models.User.login == username).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найдет"
        )
    return schemas.UserProfile(
        login=user.login,
        email=user.email,
        countryCode=user.countryCode,
        isPublic=user.isPublic,
        phone=user.phone if user.phone else None,
        image=user.image if user.image else None,
    )
