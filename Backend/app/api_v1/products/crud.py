from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.orm import Query
from app.core.models import Product, Category
from .schemas import ProductCreate,ProductUpdate,ProductPartialUpdate

async def get_all_products(
        session: AsyncSession,
        category_id: int | None = None,
        min_price: int | None = None,
        max_price: int | None = None
) -> list[Product]:
    stmt =  select(Product)
    if category_id is not None:
        stmt = stmt.filter(Product.category_id == category_id)
    if min_price is not None:
        stmt = stmt.filter(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.filter(Product.price <= max_price)
        
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)

async def get_categories(
        session: AsyncSession
) -> list[Category]:
    result = await session.execute(select(Category))
    return result.scalars().all()

async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product_in: ProductCreate) -> ProductCreate:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product

async def update_product(
        session:  AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductPartialUpdate,
        partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)
    await session.commit()
    return product

async def delete_product(
        session: AsyncSession,
        product: Product,
) -> None:
    await session.delete(product)
    await session.commit()

async def create_product_category(
        session: AsyncSession,
        category_name: str
):
    new_category = Category(name = category_name)
    session.add(new_category)
    await session.commit()
    return new_category
    