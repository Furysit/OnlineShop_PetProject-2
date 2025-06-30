from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.models import db_helper, User
from .schemas import UserCreate, UserOut
from fastapi import status
from . import crud
from .dependecies import get_user_by_id, get_current_user
from ..mail_send import send_forgot_password
from .auth import create_forgot_password_token
from sqlalchemy import delete

RESET_TOKEN_EXPIRE_MINUTES = 5

router = APIRouter(tags=["Users"],prefix="/users")


@router.get("/get_users",
            response_model=list[UserOut],
            status_code=status.HTTP_200_OK,
            summary="Получить всех пользователей",
            description="Пока для всех, но потом для админа будет"
            
            )
async def get_all_users(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
):
    return await crud.get_all_users(session=session)


@router.post("/create",
            response_model=UserOut,
            status_code=status.HTTP_201_CREATED,
            summary="Создать пользователя",
            description="Создает пользователя admin/user"
                )
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
):
    return await crud.create_user(session=session, user_in=user_in)

@router.get("/me",
            status_code=status.HTTP_200_OK,
            summary="Проверка авторизации",
            description="Проверяет авторизован ли пользователь по JWT")
async def read_me(
    current_user: User = Depends(get_current_user)
    ):
    return f"{current_user.email} is authorized"


@router.get("/{user_id}",
            response_model=UserOut,
            status_code=status.HTTP_200_OK,
            summary="Получить пользователя по id",
            description="Отдает пользователя с заданым id")
async def get_user(
    user: User = Depends(get_user_by_id)
):
    return user

@router.delete("/delete/{user_id}",
            response_model=None,
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Удалить пользователя",
            description="Удаляет пользователя с заданым id")
async def delete_user(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_user_by_id)
)-> None:   
    return await crud.delete_user(
        session=session,
        user=user
    )

@router.post("/forgot_password", 
             response_model=None, 
             status_code=status.HTTP_204_NO_CONTENT,
             summary="Сброс пароля",
            description="Сбрасывает пароль и отправляет JWT токен для смены пароля")
async def forgot_password(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_user_by_id)
) -> None:
    access_token_expires = timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    token = create_forgot_password_token(data={"sub": str(user.id)},expires_delta=access_token_expires)
    send_forgot_password(username=user.username, user_id=user.id, user_email=user.email, token=token)


