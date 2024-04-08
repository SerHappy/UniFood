from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_verified: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
