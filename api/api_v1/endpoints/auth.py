from fastapi import APIRouter, Depends, status, HTTPException
from api.dependencies import get_db
from config.security import verify_password
from config.setting import setting
from schemas.auth import LoginSchema
from sqlalchemy.orm import Session
from datetime import timedelta, date
from config.security import create_access_token
from custom_errors.http_errors.http_base_error import (
    NotFoundError,
    CustomError,
    ConflictError,
    AutherizationError,
)
from models.user import User
import crud

router = APIRouter()


@router.post("/login", status_code=(status.HTTP_201_CREATED))
def login(login_schema: LoginSchema, db: Session = Depends(get_db)):
    """
    Pass username and password it will return the jwt token
    """
    user: User = crud.user.get_by_email(db, email=login_schema.email.lower())
    if not user:
        raise NotFoundError(
            [
                CustomError(
                    error_loc=["not_found", "user"],
                    error_object=Exception(
                        "User Does Not Exist Please Reach Out To Admin"
                    ),
                )
            ]
        )
    is_password_valid = verify_password(login_schema.password, user.password)
    if not is_password_valid:
        raise ConflictError(
            [
                CustomError(
                    error_loc=["conflict", "username or password"],
                    error_object=Exception("Please Check Username or Password"),
                )
            ]
        )
    if user.status != 1:
        raise AutherizationError(
            [
                CustomError(
                    error_loc=["unautherized"],
                    error_object=Exception("Account Is Deactivated"),
                )
            ]
        )

    if not user.is_super_admin:
        is_user_expired = user.expiry_date < date.today()
        if is_user_expired:
            raise AutherizationError(
                [
                    CustomError(
                        error_loc=["unautherized"],
                        error_object=Exception(
                            "Plan Is Expired Please Reach Out To Admin"
                        ),
                    )
                ]
            )

    claim = {"email": user.email, "id": user.id, "is_super_admin": user.is_super_admin}
    token = create_access_token(
        claim, expires_delta=timedelta(minutes=(setting.ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    return {"token": token}
