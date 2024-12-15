from app.dao.base import BaseDAO
from app.categories.models import Category

class CategoryDAO(BaseDAO):
    model = Category