from typing import Any, Dict, List, Optional, Union
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.security import get_password_hash
from sqlalchemy import func
from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate
from datetime import datetime, timedelta


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def get_not_admin(self, db: Session, id: Any) -> Optional[User]:
        return (
            db.query(User).filter(User.id == id, User.is_super_admin == False).first()
        )

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(func.lower(User.email) == email).first()

    def get_by_id(self, db: Session, *, id: int) -> Optional[User]:
        return db.query(User).filter(User.id == id).first()

    def create(self, db: Session, *, obj_in: UserCreate, created_by=None) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["expiry_date"] = datetime.now() + timedelta(90)
        obj_in_data["created_by"] = created_by
        obj_in_data["created_date"] = datetime.now()

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[User, Dict[str, Any]],
        modified_by=None
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(
            db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by
        )

    def is_superuser(self, user: User) -> bool:
        return user.is_admin

    def get_none_admin_user(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        return (
            db.query(self.model)
            .filter(User.is_super_admin == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_testing_user(self, db: Session):
        return db.query(self.model).all()


user = CRUDUser(User)
