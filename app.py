from fastapi import APIRouter, Depends, FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from api.dependencies import get_current_user
from config.setting import Setting, get_settings
from api.api_v1 import api_v1
from db.model.user import UserModel
from middlewares.auth_middleware import AuthMiddleWare
import logging.config
from pathlib import Path
from fastapi.responses import JSONResponse
from custom_errors.http_errors.http_base_error import (
    AutherizationError,
    BadRequestError,
    ConflictError,
    CustomError,
    InternalServerError,
    NotFoundError,
    PermissionDeniedError,
)
import json
import sys
import traceback

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

BASE_PATH = Path(__file__).resolve().parent


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        ex_type, ex, tb = sys.exc_info()
        print(e.with_traceback(tb))
        print(traceback.format_exc())
        if isinstance(e, BadRequestError):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": json.loads(e.json())},
            )
        elif isinstance(e, InternalServerError):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": json.loads(e.json())},
            )
        elif isinstance(e, AutherizationError):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": json.loads(e.json())},
            )
        elif isinstance(e, PermissionDeniedError):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"detail": json.loads(e.json())},
            )
        elif isinstance(e, NotFoundError):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": json.loads(e.json())},
            )
        elif isinstance(e, ConflictError):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"detail": json.loads(e.json())},
            )
        else:
            exception_ = InternalServerError(
                errors=[
                    CustomError(
                        error_loc=["internal_server"],
                        error_object=Exception("Some error occured. Contact to admin"),
                    )
                ]
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": json.loads(exception_.json())},
            )


root_router = APIRouter()
app = FastAPI()
origins = ["http://localhost:3000"]

# DO NOT CHANAGE the position of the middleware
app.add_middleware(AuthMiddleWare)
app.middleware("http")(catch_exceptions_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@root_router.get("/")
def hello_world(setting: Setting = Depends(get_settings)):
    print(setting.APP_NAME)
    return {"message": "Hello World!"}


@root_router.get("/get-chart-data")
def get_chart_data(user: UserModel = Depends(get_current_user)):
    print("=========================")
    print(user)
    return {
        "scatter": {"x": [1, 2, 4], "y": [2, 6, 3]},
        "bar": {"x": [1, 2, 3, 4], "y": [2, 5, 3, 8]},
    }


app.include_router((api_v1.route_v1), prefix="/api/v1")
app.include_router(root_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
