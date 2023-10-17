from crud.base import CRUDBase
from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate, DocumentUpdate
from typing import Any, Dict, Union

class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    def get(self, db: Session, id: Any):
        return db.query(Document).filter(Document.id == id,Document.status == 1).first()
    
    def create_document(self, db: Session, *, name:str, static_file_path:str, actual_file_path:str):
        # obj_in_data = jsonable_encoder(obj_in)
        db_obj = Document()
        print(db_obj)
        # db_obj.created_by = created_by
        # db.user_id =  user_id
        db_obj.name = name
        db_obj.actual_file_path = actual_file_path
        db_obj.static_file_path = static_file_path
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


    def update_document(
        self, db: Session, *, db_obj: Document, obj_in: Union[Document, Dict[str, Any]], modified_by=None
    ) -> Document:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data, modified_by=modified_by)

    def delete_document():
        return "delete document"
    
document = CRUDDocument(Document)
