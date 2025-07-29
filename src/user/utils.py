from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
import jwt

load_dotenv()

SECRET_KEY = getenv("AUTH_SECRET_KEY")
ALGORITHM = getenv("AUTH_ALGORITHM")
ACCESS_TOKEN_TIME_MINUTES = int(getenv("AUTH_TOKEN_TIME_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    except jwt.PyJWTError:
        return None