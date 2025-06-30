from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select, update, delete
from app.core.models import User, Order, OrderItem



async def get_all_ordrers(
        session: AsyncSession,
        admin: User
) -> list[Order]:
    stmt = select(Order)
    result = await session.execute(stmt)
    orders = result.scalars().all()

    return orders

async def get_all_users(
        session: AsyncSession,
        admin: User
) -> list[User]:
    stmt = select(User)
    result = await session.execute(stmt)
    users = result.scalars().all()

    return users


async def delete_all_orders(session: AsyncSession):
    # Сначала удалить все OrderItem
    await session.execute(delete(OrderItem))
    # Затем удалить все Order
    await session.execute(delete(Order))
    await session.commit()
