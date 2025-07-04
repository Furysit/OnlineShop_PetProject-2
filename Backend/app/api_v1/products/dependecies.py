from typing import Annotated
from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models import db_helper, Product
from . import crud

async def product_by_id(
        product_id : Annotated[int, Path],
        session: AsyncSession = Depends(db_helper.scoprd_session_dependecy)
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Not found!"
    )