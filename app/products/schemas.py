from pydantic import BaseModel, Field, ConfigDict

class SProductAdd(BaseModel):

    product_name: str = Field(..., description="Название товара")
    product_img: str = Field(..., description="Фото товара")
    product_description: str = Field(..., description="Название товара")
    product_sizes: str = Field(..., description="Размеры товара")
    product_price: int = Field(1, description="Цена товара")
    category: str = Field(..., description="Категория товара")

class SProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_name: str = Field(..., description="Название товара")
    product_img: str = Field(..., description="Фото товара")
    product_description: str = Field(..., description="Название товара")
    product_sizes: str = Field(..., description="Размеры товара")
    product_price: int = Field(1, description="Цена товара")
    category: str = Field(..., description="Категория товара")