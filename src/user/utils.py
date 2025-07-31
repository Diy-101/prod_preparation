from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt

from datetime import datetime, timedelta

import src.user.models as models
import src.user.schemas as schemas
from src.database import get_db
from src.config import auth_settings

SECRET_KEY = auth_settings.secret_key
ALGORITHM = auth_settings.algorithm
TOKEN_TIME_MINUTES_EXPIRATION = auth_settings.token_time_minutes_expiration

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/sign-in")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=TOKEN_TIME_MINUTES_EXPIRATION)
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
