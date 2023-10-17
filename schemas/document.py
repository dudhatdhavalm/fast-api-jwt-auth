from typing import Optional, List
from pydantic import BaseModel


class DocumentBase(BaseModel):
    name: str
    static_file_path: str
    actual_file_path: Optional[str] = None


class DocumentCreate(DocumentBase):
    ...
    class Config:
        orm_mode = True


class DocumentInDBBase(DocumentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Document(DocumentInDBBase):
    pass


# class DocumentWithoutActual(BaseModel):
#     name: str
#     static_file_path: str
#     id: int
#     created_by: Optional[str] = None
#     status: int

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    static_file_path: Optional[str] = None
    actual_file_path: Optional[str] = None
    id: int


class DocumentStatusUpdate(DocumentUpdate):
    status: Optional[int] = None


class DocumentOnly(DocumentInDBBase):
    ...


class DocumentSearch(BaseModel):
    startAt: int
    pageSize: int
    sortDesc: bool

class DocumentWithoutActual(BaseModel):
    name: str
    static_file_path: str
    id: int
    created_by: Optional[str] = None
    status: int


class DocumentSearchResults(DocumentSearch):
    items: List[Document] = []
