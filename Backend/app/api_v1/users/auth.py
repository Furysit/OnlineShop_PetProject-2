from jose import JWTError, jwt 
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.models import db_helper, User
from .schemas import UserLogin, TokenWithUser, LoginRequest
from . import crud



SECRET_KEY = 'secret'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

router = APIRouter(tags=["Auth"])



def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or datetime(minutes=15))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_forgot_password_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or datetime(minutes=5))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed:str) -> str:
    return pwd_context.verify(plain_password, hashed)


@router.post("/login", 
            response_model=TokenWithUser,
            summary="Вход пользователя",
            description="Возвращает JWT токен при успешной авторизации"
            )
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
):
    user = await crud.authenticate_user(session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token,
            "token_type": "bearer",
            "user" : {
                "id" : user.id,
                "email" : user.email,
                "role" : user.role
            }}




@router.post("/reset_password",
            status_code=status.HTTP_200_OK,
            summary="Сброс пароля",
            description="Функция для сброса пароля, возвращает сообщение при успешном сбросе пароля")
async def reset_password(
    token: str,
    new_password: str,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid token or time is out")
    
    hashed_password = pwd_context.hash(new_password)
    await crud.update_user_password(session, user_id=int(user_id), new_password=hashed_password)
    return {"msg": "Password reset successful"}