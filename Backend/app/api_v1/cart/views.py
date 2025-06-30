from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import db_helper,User
from .schemas import Cart, CartAddRequest, Cart_ext
from . import crud
from app.api_v1.products.schemas import Product
from app.api_v1.users.dependecies import get_user_by_id, get_current_user
from app.api_v1.products.dependecies import product_by_id

router = APIRouter(tags=["Cart"])

@router.get("/get_cart",
            response_model=list[Cart],
            status_code=status.HTTP_200_OK,
            summary="Получить корзину заданного пользователя",
            description="Возвращает корзину со списком товаров пользователя")
async def get_cart(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
) -> list[Cart]:
    return await crud.get_cart(session=session, user_id=user.id)

@router.post("/add",
            response_model=Cart,
            status_code=status.HTTP_201_CREATED,
            summary="Добавить товар в корзину",
            description="Добавляет товар в корзину пользователя"
            )
async def add_product_to_cart(
    data: CartAddRequest,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user),
    
) -> Cart:
    product = await product_by_id(data.product_id, session=session)
    return await crud.add_product_to_cart(session=session, user_id=user.id, product_id=product.id, quantity=data.quantity)

@router.delete("/remove_from_cart",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Удалить товар из корзины",
            description="Удаляет товар из корзины пользователя")
async def remove_from_cart(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user),
    product: Product = Depends(product_by_id)
) -> None:
    await crud.remove_product_from_cart(session=session, user_id=user.id, product_id=product.id)

@router.delete("/clear_cart",
               status_code=status.HTTP_204_NO_CONTENT,
               summary="Очистить корзину",
               description="Очищает корзину пользователя")
async def clear_cart(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
) -> None:
    await crud.clear_cart(session=session, user_id=user.id)
    

@router.get("/get_cart_detailed",
             response_model=list[Cart_ext],
             status_code=status.HTTP_200_OK,
             summary="Посмотреть детально корзину",
             description="Возвращает детальную информацию о корзине")
async def get_cart_ext(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
) -> list[Cart_ext]:
    return await crud.get_cart_ext(session=session, user_id=user.id)


@router.put("/change_quantity", status_code=200)
async def change_quantity(
    product_id: int = Query(...),
    quantity: int = Query(...),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    user: User = Depends(get_current_user)
):
    if quantity < 1:
        raise HTTPException(status_code=400, detail="Минимум 1 шт.")

    await crud.change_cart_quantity(session, user_id=user.id, product_id=product_id, quantity=quantity)
    return {"detail": "Количество обновлено"}