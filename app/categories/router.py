from fastapi import APIRouter
from app.categories.schemas import SCategoryAdd, SCategory
from app.categories.dao import CategoryDAO

router = APIRouter(prefix='/categories', tags=['Работа с категориями'])

@router.get('/')
async def get_categories():
    check = await CategoryDAO.find_all()

    if check:
        return check
    else:
        return {
            'message': "Ошибка получения списка категорий"
        }

@router.get('/{category_id}')
async def get_category_by_id(category_id: int) -> SCategory | dict:
    check = await CategoryDAO.find_by_id(category_id)

    if check:
        return check
    else:
        return {
            'message': f"Категория с таким ID не найдена"
        }

@router.post('/add')
async def add_category(category: SCategoryAdd) -> dict:
    check = await CategoryDAO.add(**category.dict())

    if check:
        return {
            'message': "Категория успешно добавлена"
        }
    else:
        return {
            'message': "Ошибка при добавлении категории"
        }

@router.post('/delete{category_id}')
async def delete_category(category_id: int) -> dict:
    check = await CategoryDAO.delete(id=category_id)

    if check:
        return {
            'message': f'Категория с ID {category_id} удален!'
        }
    else:
        return {
            'message': 'Ошибка при удалении категории'
        }
