from fastapi import APIRouter
from app.products.dao import ProductDAO
from app.products.schemas import SProduct

router = APIRouter(prefix='/products', tags=['Работа с продуктами'])

@router.get('/')
async def get_products():
    check = await ProductDAO.find_all_products()

    if check:
        return check
    else:
        return {
            'message': 'Ошибка при получении списка товара'
        }

@router.get('/{product_id')
async def get_product(product_id: int) -> SProduct | dict:
    check = await ProductDAO.find_product_by_id(product_id)

    if check is None:
        return {
            'message': f"Товар с ID {product_id} не найден"
        }

@router.post('/add')
async def add_category(product: SProduct) -> dict:
    check = await ProductDAO.add(**product.dict())

    if check:
        return {
            'message': "Категория успешно добавлена"
        }
    else:
        return {
            'message': "Ошибка при добавлении категории"
        }

@router.post('/delete{product_id}')
async def delete_category(product_id: int) -> dict:
    check = await ProductDAO.delete(id=product_id)

    if check:
        return {
            'message': f'Категория с ID {product_id} удален!'
        }
    else:
        return {
            'message': 'Ошибка при удалении категории'
        }
