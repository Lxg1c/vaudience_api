from pydantic import BaseModel, Field, ConfigDict


class SCategoryAdd(BaseModel):
    category_name: str = Field(..., description='Название категории')
    count_products: int = Field(..., description='Количество товара категории')

class SCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_name: str = Field(..., description="Название категории")
    count_products: int = Field(..., description="Количество товара данной категории")