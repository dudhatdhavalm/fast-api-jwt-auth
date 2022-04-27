from typing import Optional
from config.security import get_password_hash
from config.setting import get_settings
from db.model.user import UserModel
from schemas.auth import RegisterSchema
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import jwt

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).all()


def get_user_by_email_active(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email, UserModel.is_active == True, UserModel.expiry_date >= datetime.today()).all()


def create_user(db: Session, register_schema: RegisterSchema):
    password_hash = get_password_hash(register_schema.password)
    expiry_date = datetime.now() + timedelta(90)
    user = UserModel(name=(register_schema.name), password=password_hash, email=(register_schema.email),
      expiry_date=expiry_date)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_access_token(claim: dict, expires_delta: Optional[timedelta]=None):
    setting = get_settings()
    to_encode = claim.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    jwt_token = jwt.encode(to_encode, setting.secret_key, setting.algorithm)
    return jwt_token


def decode_access_token(token):
    setting = get_settings()
    payload = None
    try:
        payload = jwt.decode(token, setting.secret_key, setting.algorithm)
    except Exception as e:
        try:
            print('Problem with token decode => ', str(e))
        finally:
            e = None
            del e

    return payload
