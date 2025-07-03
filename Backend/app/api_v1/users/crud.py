from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update
from app.core.models import User
from .schemas import UserCreate
from .auth import hash_password, verify_password



async def create_user(session: AsyncSession,
                    user_in: UserCreate,):
    stmt = select(User).where(User.email == user_in.email)
    result: Result = await session.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists")
    
    hashed_password = hash_password(user_in.password)
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        role = user_in.role  
    )
    session.add(user)
    await session.commit()
    return user

async def get_all_users(
        session: AsyncSession
) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)

async def get_user_by_id(
        session: AsyncSession,
        user_id: int
) -> User:
    return await session.get(User, user_id)

async def get_user_by_email(
        session: AsyncSession,
        user_email: str
) -> User:
    stmt = select(User).where(User.email == user_email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none() 
    return user

async def delete_user(
          session: AsyncSession,
          user: User
): 
    await session.delete(user)

async def authenticate_user(
        session: AsyncSession,
        email:str, 
        password: str) -> User | None:
        
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

async def update_user_password(
        session: AsyncSession,
        user_id: int,
        new_password :str
):
    stmt = update(User).where(User.id == user_id).values(hashed_password = new_password)
    await session.execute(stmt)
    await session.commit()




