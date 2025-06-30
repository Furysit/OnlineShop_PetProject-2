
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.core.models import Cart, Product
from .schemas import Cart_ext

async def get_cart(
        session: AsyncSession,
        user_id: int, 
) -> list[Cart]:
    stmt = select(Cart).where(Cart.user_id == user_id)
    result = await session.execute(stmt)
    user_cart = result.scalars().all()
    return user_cart


async def add_product_to_cart(
        session: AsyncSession,
        user_id: int ,
        product_id: int,
        quantity: int = 1 
) -> Cart:
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    result = await session.execute(stmt)
    existing_item = result.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += quantity
    else:
        existing_item = Cart(user_id = user_id, product_id = product_id, quantity = quantity)
        session.add(existing_item)

    await session.commit()
    return existing_item

async def remove_product_from_cart(
        session: AsyncSession,
        user_id: int ,
        product_id: int 
) -> None:
    stmt = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    result = await session.execute(stmt)
    item = result.scalar_one_or_none()

    if item is not None:
        await session.delete(item)
        await session.commit()
    
async def clear_cart(
        session: AsyncSession,
        user_id: int,
) -> str:
    await session.execute(delete(Cart).where(Cart.user_id == user_id))
    await session.commit()
    
async def get_cart_ext(
        session: AsyncSession,
        user_id: int
        
) -> list[Cart_ext]:
    stmt = select(Cart).options(selectinload(Cart.product)).where(Cart.user_id == user_id)
    result = await session.execute(stmt)
    cart = result.scalars().all()

    return cart

async def change_cart_quantity(session: AsyncSession, user_id: int, product_id: int, quantity: int):
    stmt = update(Cart).where(
        Cart.user_id == user_id,
        Cart.product_id == product_id
    ).values(quantity=quantity)
    await session.execute(stmt)
    await session.commit()