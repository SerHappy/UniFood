from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr
    is_verified: bool = False


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase):
    password: str
