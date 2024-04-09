from app.api.deps import SessionDep
from app.db import crud
from app.schemas.messages import Message
from app.schemas.users import UserCreate, UserPublic, UserRegister
from app.services.mail import (
    generate_confirmation_email,
    generate_confirmation_token,
    send_email,
    verify_confirmation_token,
)
from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException

router = APIRouter()


@router.post("/", response_model=UserPublic)
async def create_user(
    session: SessionDep, user_in: UserRegister, background_tasks: BackgroundTasks
) -> UserPublic:
    user = await crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_create = UserCreate(**user_in.model_dump())
    user = await crud.create_user(session=session, user=user_create)
    html = generate_confirmation_email(generate_confirmation_token(user.email))
    background_tasks.add_task(
        send_email,
        user.email,
        "Подтвердите электронную почту",
        html,
    )
    return user


@router.get("/confirm")
async def confirm_email(session: SessionDep, token: str) -> Message:
    email = verify_confirmation_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="User already verified")
    await crud.verify_user(session=session, user=user)
    return Message(message="Почта подтверждена")
