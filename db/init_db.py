import sys

sys.path.insert(0, '/mnt/BA504CE3504CA7C9/Work/React Native/Workplace/fast-api-jwt-auth')
import logging
from sqlalchemy.orm import Session
from schemas.user import UserCreate
import crud
from copy import copy
from db.session import SessionLocal

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email="admin@admin.com")
    if not user:
        user_in = UserCreate(
            name="root_admin",
            email="admin@admin.com",
            password="admin@123",
            is_super_admin=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        user_data = copy(user)
        user_data.modified_by = user.id
        user_data.created_by = user.id
        user = crud.user.update(
            db, db_obj=user, obj_in=user_data.__dict__, modified_by=user.id
        )


if __name__ == "__main__":
    db = SessionLocal()
    init_db(db)
    db.close()
