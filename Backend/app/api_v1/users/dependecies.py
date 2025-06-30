from typing import Annotated
from jose import JWTError, jwt 
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from app.core.models import db_helper, User
from . import crud
from .auth import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")  

async def get_user_by_id(
        user_id: Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
) -> User: 
    user = await crud.get_user_by_id(session, user_id)
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found!"
    )


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
) -> User:
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
             raise credentials_exception
        
        user = await get_user_by_id(int(user_id), session)
        if user is None:
            raise credentials_exception
        
        return user

async def admin_required(
          user: User = Depends(get_current_user)
) -> User:
     if user.role != "admin":
          raise HTTPException(
               status_code=status.HTTP_403_FORBIDDEN,
               detail="Not allowed"
          )
     return user