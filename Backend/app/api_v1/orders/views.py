from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.core.models import db_helper, Cart, User
from fastapi import status
from . import crud

from app.api_v1.orders.schemas import Order
from app.api_v1.users.dependecies import get_user_by_id, get_current_user, admin_required
from app.api_v1.products.dependecies import product_by_id
from app.api_v1.mail_send import sendmessage
from app.api_v1.cart.dependecies import get_cart_by_user_id

router = APIRouter(tags=["Orders"])

@router.get("/my_orders",
            response_model= list[Order],
            status_code=status.HTTP_200_OK,
            summary="Получить список всех заказов",
            description="Возвращает список всех заказов заданного пользователя")
async def get_orders(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
):
    return await crud.get_orders(session=session, user_id=user.id)


@router.post("/create_order", 
            response_model=Order, 
            status_code=status.HTTP_201_CREATED,
            summary="Создание заказа",
            description="Берет все товары из корзины и создает заказ. Отсылает сообщение на почту.")
async def create_order(
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
):  
    cart_items = await get_cart_by_user_id(session, user_id=user.id)
    if not cart_items:
        raise HTTPException(status_code=400, detail="Корзина пуста")

    order = await crud.create_order(session=session, user_id=user.id)
    await session.execute(delete(Cart).where(Cart.user_id == user.id))
    await session.commit()

    print("📧 Отправка сообщения...")
    background_tasks.add_task(
    sendmessage,
    username=user.username,
    order_id=order.id,
    total=order.total_price
)
    
    print("📧 Отправлено")
    return order


@router.get("/get_order/{order_id}", 
            response_model= Order,
            status_code=status.HTTP_200_OK,
            summary="Получить заданный заказ",
            description="Возвращает заказ с подробной информацией о продукте")
async def get_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
):
    return await crud.get_order(session=session, order_id=order_id)