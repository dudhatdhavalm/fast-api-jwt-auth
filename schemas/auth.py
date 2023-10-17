from pydantic import BaseModel

class LoginSchema(BaseModel):
    email = None
    email: str
    password = None
    password: str


class RegisterSchema(LoginSchema):
    name = None
    name: str

    class Config:
        orm_mode = True
