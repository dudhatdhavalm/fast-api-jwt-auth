from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    skill: Optional[List[str]] = None
    document_id: Optional[int] = None
    addr: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    english_proficiency : Optional[int] = None
    last_education: Optional[str] = None

    status: int = 1


class UserCreate(UserBase):
    first_name: str
    email: EmailStr
    status: int = 1
    addr: str
    skill: List[str]
    city: str
    state: str
    english_proficiency : int
    last_education: str

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    id: int


class UserDelete(UserBase):
    id: int


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class UserOnly(UserInDBBase):
    ...


class UserSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool

class UserDocumentSchema(UserBase):
    id: int
    document_id: int
    static_file_path: str

class AllUserWithDoc(BaseModel):
    items: List[UserDocumentSchema] = []

