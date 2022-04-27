from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.dependencies import get_current_user
from config.setting import Setting, get_settings
from api.api_v1 import api_v1
from db.model.user import UserModel
from middlewares.auth_middleware import AuthMiddleWare
root_router = APIRouter()
app = FastAPI()
origins = [
    'http://localhost:3000']
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=[
                       '*'],
                   allow_headers=[
                       '*'])
app.add_middleware(AuthMiddleWare)


@root_router.get('/')
def hello_world(setting: Setting = Depends(get_settings)):
    print(setting.app_name)
    return {'message': 'Hello World!'}


@root_router.get('/get-chart-data')
def get_chart_data(user: UserModel = Depends(get_current_user)):
    print('=========================')
    print(user)
    return {'scatter': {'x': [
        1, 2, 4],
        'y': [
        2, 6, 3]},
        'bar': {'x': [
            1, 2, 3, 4],
        'y': [2, 5, 3, 8]}}


app.include_router((api_v1.route_v1), prefix='/api/v1')
app.include_router(root_router)
