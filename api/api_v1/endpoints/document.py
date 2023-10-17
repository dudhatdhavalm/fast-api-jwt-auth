from fastapi import APIRouter, Depends, UploadFile, Form , HTTPException
from sqlalchemy.orm import Session
from api import dependencies
import uuid
from PIL import Image
import os
from schemas.document import DocumentWithoutActual
import crud
from util.directory_helper import generate_file_name, create_document_directory
router = APIRouter()


@router.post('', status_code=200)
def upload_document(
    *,
    db: Session = Depends(dependencies.get_db),
    image: UploadFile = Form()
):
    open_image = Image.open(image.file)
    print(image)
    base_directory = "./static/"
    
    name = generate_file_name(".png")
    folder_path = create_document_directory(base_directory, 'resume')

    static_file_path = os.path.join(folder_path, name)
    open_image.save(static_file_path)

    document = crud.document.create_document(
        db=db, name=name, static_file_path=static_file_path,actual_file_path=None)
    
    return document

@router.get('/{document_id}',status_code=200,response_model=DocumentWithoutActual)
def fetch_document(
    *,
    db: Session = Depends(dependencies.get_db),
    document_id : int
) -> DocumentWithoutActual:
    
    result = crud.document.get(db=db,id=document_id)
    if not result:
        raise HTTPException(
            status_code=404, detail=f"Document with ID {document_id} not found"
        )

    response = DocumentWithoutActual(id=result.id, name=result.name,
                                     static_file_path=result.static_file_path, created_by=result.created_by, status=result.status)

    return response

@router.delete("/{document_id}", status_code=200)
def delete_document(
    *,
    document_id: int,
    db: Session = Depends(dependencies.get_db)
) -> dict:
    """
    Delete document
    """
    result = crud.document.get(db=db, id=document_id)
    result.status = 0
    db.commit()

    return 'Document Deleted successfully'