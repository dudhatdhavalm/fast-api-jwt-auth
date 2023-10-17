from fastapi import APIRouter, Depends
from core.security import reusable_oauth2
from api.api_v1.endpoints import auth , user , document

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/user",
                          tags=["user"], dependencies=[Depends(reusable_oauth2)])
api_router.include_router((document.router) , prefix='/document', tags=['document'])
