from fastapi import APIRouter, Depends, status, HTTPException
from api.dependencies import get_db
from config.security import verify_password
from schemas.user import UserCreate, UserOnly
from sqlalchemy.orm import Session
from models.user import User
import crud

router = APIRouter()


@router.post(
    "",
    response_model=UserOnly,
    response_model_exclude={"password"},
    status_code=(status.HTTP_201_CREATED),
)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Register new user to system
    """
    existing_users = crud.user.get_by_email(db, email=user_create.email.lower())
    if len(existing_users) != 0:
        raise HTTPException(
            status_code=(status.HTTP_409_CONFLICT), detail="Email already exist"
        )
    user = crud.user.create(db, user_create)
    return user
