from passlib.context import CryptContext
from fastapi.security import HTTPBearer
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)

def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_context.hash(password)
