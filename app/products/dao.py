from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.products.models import Product

class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    async def find_all_products(cls):
        async with async_session_maker() as session:

            query = select(cls.model).options(joinedload(cls.model.category))
            result = await session.execute(query)

            products_info = result.scalars().all()

            products_data = []

            for product in products_info:
                product_dict = product.to_dict()
                product_dict['category'] = product.category.name if product.category else None
                products_data.append(product_dict)

            return products_data

    @classmethod
    async def find_product_by_id(cls, product_id):
        async with async_session_maker() as session:

            query = select(cls.model).options(joinedload(cls.model.category)).filter_by(id=product_id)
            result = await session.execute(query)
            product_info = result.scalars().all()

            if not product_info:
                return None

            product_data = product_info.to_dict()
            product_data['category'] = product_info.category.name if product_info.category else None
            return product_data