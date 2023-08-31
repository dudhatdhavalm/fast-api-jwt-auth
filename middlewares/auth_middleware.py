from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from db.database import SessionLocal
from services.user_service import decode_access_token, get_user_by_email_active
from custom_errors.http_errors.http_base_error import AutherizationError, CustomError


class AuthMiddleWare(BaseHTTPMiddleware):
    allow_urls = ["/api/v1/auth/login", "/register", "/"]

    async def dispatch(self, request: Request, call_next):
        current_url = request.url.path
        if current_url in AuthMiddleWare.allow_urls:
            return await call_next(request)
        token = request.headers.get("Authorization", None)
        if token == None:
            raise AutherizationError(
                [
                    CustomError(
                        error_loc=["unautherized"],
                        error_object=Exception("authentication header missing"),
                    )
                ]
            )
        claim = decode_access_token(token)
        if claim == None:
            raise AutherizationError(
                [
                    CustomError(
                        error_loc=["unautherized"],
                        error_object=Exception("invalid authentication token"),
                    )
                ]
            )
        email = claim.get("email", None)
        if email == None:
            raise AutherizationError(
                [
                    CustomError(
                        error_loc=["unautherized"],
                        error_object=Exception("invalid authentication token"),
                    )
                ]
            )
        db = None

        try:
            db = SessionLocal()
            user = get_user_by_email_active(db, email)
            if not user:
                raise AutherizationError(
                    [
                        CustomError(
                            error_loc=["unautherized"],
                            error_object=Exception("user not found"),
                        )
                    ]
                )
            request.state.current_user = user
        except Exception as e:
            print(str(e))
            raise e
        finally:
            if db != None:
                db.close()
        return await call_next(request)
