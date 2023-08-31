from fastapi import APIRouter, Depends, status, HTTPException
from api.dependencies import get_db
from config.security import verify_password
from config.setting import get_settings
from schemas.auth import LoginSchema, RegisterSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from services.user_service import create_access_token, create_user, get_user_by_email

router = APIRouter()


@router.post("/login", status_code=(status.HTTP_201_CREATED))
def login(login_schema: LoginSchema, db: Session = Depends(get_db)):
    """
    Pass username and password it will return the jwt token
    """
    existing_users = get_user_by_email(db, login_schema.email)
    if len(existing_users) == 0:
        raise HTTPException(
            status_code=(status.HTTP_404_NOT_FOUND), detail="User does not exist."
        )
    user = existing_users[0]
    is_password_valid = verify_password(login_schema.password, user.password)
    if not is_password_valid:
        raise HTTPException(
            status_code=(status.HTTP_409_CONFLICT),
            detail="Please check username and password.",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=(status.HTTP_401_UNAUTHORIZED),
            detail="Your account is deactivated.",
        )

    is_user_expired = user.expiry_date < date.today()
    if is_user_expired:
        raise HTTPException(
            status_code=(status.HTTP_401_UNAUTHORIZED),
            detail="Please upgrade your plan.",
        )
    claim = {"email": user.email, "id": user.id}
    setting = get_settings()
    token = create_access_token(
        claim, expires_delta=timedelta(minutes=(setting.ACCESS_TOKEN_EXPIRE_MINUTES))
    )
    return {"token": token}


@router.post(
    "/register",
    response_model=RegisterSchema,
    response_model_exclude={"password"},
    status_code=(status.HTTP_201_CREATED),
)
def register(register_schema: RegisterSchema, db: Session = Depends(get_db)):
    """
    Register new user to system
    """
    existing_users = get_user_by_email(db, register_schema.email)
    if len(existing_users) != 0:
        raise HTTPException(
            status_code=(status.HTTP_409_CONFLICT), detail="Email already exist"
        )
    user = create_user(db, register_schema)
    return user
