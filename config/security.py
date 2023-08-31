from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
from config.setting import setting
from jose import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
PREFIX = "Bearer"


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)


def create_access_token(claim: dict, expires_delta: Optional[timedelta] = None):
    to_encode = claim.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)
    return jwt_token


def decode_access_token(token):
    payload = None
    try:
        auth_token = get_token(token)
        payload = jwt.decode(auth_token, setting.SECRET_KEY, setting.ALGORITHM)
    except Exception as e:
        print("Problem with token decode => ", str(e))
    return payload


def get_token(header):
    bearer, _, token = header.partition(" ")
    if bearer != PREFIX:
        raise ValueError("Invalid token")

    return token
