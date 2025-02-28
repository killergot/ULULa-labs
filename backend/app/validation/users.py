from pydantic import BaseModel,EmailStr


class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    role: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str