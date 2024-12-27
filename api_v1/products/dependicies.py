from pathlib import Path
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from core.models import db_helper, Product
from . import crud


async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    product = await crud.get_product_by_id(session=session, product_id=product_id)

    if product is not None:
        return product

    raise HTTPException(status_code=404, detail="Product not found")
