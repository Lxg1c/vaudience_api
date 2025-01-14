"""
CREATE
READ
UPDATE
DELETE
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from .schemas import ProductCreate, ProductUpdate, ProductPartialUpdate


async def get_products(session: AsyncSession) -> list[Product]:
    statement = select(Product).order_by(Product.id)
    result: Result = await session.execute(statement)
    products = result.scalars().all()

    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(
    session: AsyncSession,
    product_in: Product,
    product_update: ProductUpdate | ProductPartialUpdate,
    partial: bool = False,
) -> Product:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product_in, name, value)
    await session.commit()
    return product_in


async def delete_product(
    session: AsyncSession,
    product_in: Product,
) -> None:
    await session.delete(product_in)
    await session.commit()
