from fastapi import status
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from custom_errors.http_errors.http_base_error import AutherizationError, CustomError
import crud
from config.security import decode_access_token


class AuthMiddleWare(BaseHTTPMiddleware):
    allow_urls = ["/api/v1/auth/login", "/docs", "/openapi.json", "/"]

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
        user_id = claim.get("id", None)
        if user_id == None:
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
            user = crud.user.get_by_id(db, user_id)
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
