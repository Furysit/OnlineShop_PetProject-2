from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi import UploadFile, File, Form
import uuid, os, shutil
from sqlalchemy import select
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate,ProductPartialUpdate, Category, CategoryCreate, CategoryOut
from app.core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import Product as ProductModel

from .dependecies import product_by_id

router = APIRouter(tags=["Products"])

@router.post("/create_category",
            response_model=CategoryOut,
            status_code=status.HTTP_201_CREATED,
            summary="Создание категории",
            description="Создает категорию и возвращает"
            )
async def create_category(
    category : CategoryCreate,
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
) -> Category:
    return await crud.create_product_category(session, category = category)
    

@router.get("/categories", response_model=list[CategoryOut])
async def get_all_categories(session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)):
    return await crud.get_categories(session=session)


@router.get("/",
            response_model=list[Product],
            status_code=status.HTTP_200_OK,
            summary="Посмотреть все товары",
            description="Возвращает список всех товаров")
async def get_products(
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
    category_id: int | None = Query(default=None, description="ID категории"),
    min_price: int | None = Query(default=None, ge=0, description="Минимальная цена"),
    max_price: int | None = Query(default=None, ge=0, description="Максимальная цена")
    ):

    return await crud.get_all_products(session=session, category_id=category_id, min_price=min_price, max_price=max_price)


@router.get("/{product_id}",
            response_model=Product,
            status_code=status.HTTP_200_OK,
            summary="Посмотреть конкретный товар",
            description="Возвращает товар по заданному id")
async def get_product(
    product: Product = Depends(product_by_id)
):

    return product

@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    summary="Создать товар с изображением",
    description="Создает товар, загружает изображение и возвращает его"
)
async def create_product_with_image(
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    image: UploadFile = File(...),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
):
    
    ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    image_path = os.path.join("static", "images", filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/static/images/{filename}"

    # Создание записи в БД
    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        image_url=image_url
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


@router.put("/{product_id}/",
            response_model=Product,
            status_code=status.HTTP_202_ACCEPTED,
            summary="Обновить товар",
            description="Полное обновление товара"
            )
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
) -> Product:
    return await crud.update_product(
        session=session,
        product=product, 
        product_update=product_update
        )

@router.patch("/{product_id}/",
            response_model=Product,
            status_code=status.HTTP_202_ACCEPTED,
            summary="Обновить товар",
            description="Частичное обновление товара"
            )
async def update_product_partial(
    product_update: ProductPartialUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy),
) -> Product:
    return await crud.update_product(
        session=session, 
        product=product, 
        product_update=product_update, 
        partial=True
        )


@router.delete("/{product_id}/",
            status_code=status.HTTP_204_NO_CONTENT,
            summary="Удалить товар",
            description="Удалить товар полностью")
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
) -> None:
    return await crud.delete_product(
        session=session,
        product=product
    )