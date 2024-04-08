from app.api.deps import SessionDep
from app.db import crud
from app.schemas.users import UserCreate, UserPublic, UserRegister
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.post("/registration", response_model=UserPublic)
async def create_user(session: SessionDep, user_in: UserRegister) -> UserPublic:
    user = await crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_create = UserCreate(**user_in.model_dump())
    user = await crud.create_user(session=session, user=user_create)
    return user
