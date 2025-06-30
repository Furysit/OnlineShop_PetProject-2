from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.models import Cart

async def get_cart_by_user_id(
        session: AsyncSession,
        user_id: int
) :
    stmt = select(Cart).where(Cart.user_id == user_id)
    result = await session.execute(stmt)

    cart = result.scalars().all()
    return cart