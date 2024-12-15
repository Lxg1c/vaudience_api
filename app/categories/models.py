from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk

# Создаем модель таблицы категорий (categories)
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int_pk]
    category_name: Mapped[str_uniq]
    count_products: Mapped[int] = mapped_column(server_default=text("0"))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

    def __str__(self):
        return f"{self.__class__.__name__} (id={self.id}, category_name={self.category_name!r})"

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            "id": self.id,
            "category_name": self.category_name,
            "count_products": self.count_products,
        }