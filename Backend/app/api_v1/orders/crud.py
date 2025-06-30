from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from .schemas import Order
from app.core.models import Order, OrderItem, Cart
from app.api_v1.cart.schemas import Cart_ext
from datetime import timezone, datetime


async def create_order(
        session: AsyncSession,
        user_id: int,
) -> Order:
    stmt = select(Cart).options(selectinload(Cart.product)).where(Cart.user_id == user_id)
    result = await session.execute(stmt)
    items_list = result.scalars().all()
    order_items = []
    for item in items_list:
        a = OrderItem(product_id = item.product_id, quantity = item.quantity)
        order_items.append(a)

    total_price = sum(item.product.price * item.quantity for item in items_list)

    new_order = Order(
        user_id=user_id,
        total_price=total_price,
        created_at=datetime.now(timezone.utc),
        order_items=order_items
    )

    session.add(new_order)
    await session.commit()
    #clear_cart будет в view
    stmt = select(Order).options(
        selectinload(Order.order_items).selectinload(OrderItem.product)
    ).where(Order.id == new_order.id)
    result = await session.execute(stmt)
    order_with_products = result.scalars().first()
    return order_with_products

async def get_orders(
    session: AsyncSession,
    user_id: int
) -> list[Order]:
    stmt =  select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.product)).where(Order.user_id == user_id)
    result = await session.execute(stmt)
    orders = result.scalars().all()

    return orders

async def get_order(
        session: AsyncSession,
        order_id: int
):
    stmt = select(Order).options(selectinload(Order.order_items).selectinload(OrderItem.product)).where(Order.id == order_id)
    result = await session.execute(stmt)
    order = result.scalar_one_or_none()
    return order