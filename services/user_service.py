from typing import Optional
from core.security import get_password_hash
from core.config import settings

from models.user import User
from schemas.auth import RegisterSchema
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).all()


def create_user(db: Session, register_schema: RegisterSchema):
    password_hash = get_password_hash(register_schema.password)
    expiry_date = datetime.now() + timedelta(90)
    user = User(name=(register_schema.name), password=password_hash, email=(register_schema.email),
      expiry_date=expiry_date)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_email_active(db: Session, email: str):
    return db.query(User).filter(User.email == email).all()
    

def create_access_token(claim: dict, expires_delta: Optional[timedelta]=None):

    to_encode = claim.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return jwt_token


def decode_access_token(token):

    payload = None
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
    except Exception as e:
        try:
            print('Problem with token decode => ', str(e))
        finally:
            e = None
            del e

    return payload
