from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_super_admin: bool = False
    status: int = 1


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_super_admin: bool


class UserUpdate(BaseModel):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserOnly(UserInDBBase):
    ...
