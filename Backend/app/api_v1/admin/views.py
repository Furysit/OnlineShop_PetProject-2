from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.core.models import db_helper, User
from app.api_v1.orders.schemas import Order
from app.api_v1.users.schemas import UserOut
from fastapi import status
from . import crud
from app.api_v1.users.dependecies import get_user_by_id, get_current_user, admin_required


router = APIRouter(tags=["admin"])

@router.get("/get_all_orders",
            response_model=list[Order],
            status_code=status.HTTP_200_OK,
            summary="Получить список всех пользователей",
            description="Возвращает список всех пользователей. Только для админа")
async def get_all_orders(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    admin: User = Depends(admin_required)
) :
    return await crud.get_all_ordrers(session=session,admin=admin)

@router.get("/get_all_users",
            response_model=list[UserOut],
            status_code=status.HTTP_200_OK,
            summary="Получить список всех заказов",
            description="Возвращает список всех заказов. Только для админа")
async def get_all_users(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    admin: User = Depends(admin_required)
) :
    return await crud.get_all_users(session=session,admin=admin)

@router.delete("/delete_all_orders",summary="Удалить все заказы")
async def delete_all_orders(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
):
    await crud.delete_all_orders(session)
    return {"message": "Все заказы удалены"}