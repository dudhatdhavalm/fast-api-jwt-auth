from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from db.database import SessionLocal
from services.user_service import decode_access_token, get_user_by_email_active

class AuthMiddleWare(BaseHTTPMiddleware):
    allow_urls = [
     '/api/v1/auth/login', '/register']

    async def dispatch(self, request: Request, call_next):
        current_url = request.url.path
        if current_url in AuthMiddleWare.allow_urls:
            return await call_next(request)
        token = request.headers.get('Authorization', None)
        if token == None:
            return JSONResponse(content={'detail': 'Authentication header missing'}, status_code=(status.HTTP_401_UNAUTHORIZED))
        claim = decode_access_token(token)
        if claim == None:
            return JSONResponse(content={'detail': 'Please check authentication token.'}, status_code=(status.HTTP_401_UNAUTHORIZED))
        email = claim.get('email', None)
        if email == None:
            return JSONResponse(content={'detail': 'Please check authentication token.'}, status_code=(status.HTTP_401_UNAUTHORIZED))
        db = None
        try:
            try:
                db = SessionLocal()
                user = get_user_by_email_active(db, email)
                request.state.current_user = user
            except Exception as e:
                try:
                    print('Database Connection Issue', str(e))
                    return JSONResponse(content={'detail': 'Please check database connection.'}, status_code=(status.HTTP_401_UNAUTHORIZED))
                finally:
                    e = None
                    del e

        finally:
            if db != None:
                db.close()

        return await call_next(request)
