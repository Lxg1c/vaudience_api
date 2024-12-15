from sqlalchemy import text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base, str_uniq, int_pk, str_null_true

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int_pk]
    product_name: Mapped[str_uniq]
    product_img: Mapped[str]
    product_description: Mapped[str]
    product_sizes: Mapped[str]
    product_price: Mapped[int]
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)

    # Определяем отношение: один продукт имеет одну категорию
    category: Mapped['Category'] = relationship('Category', back_populates='products')

    def __str__(self):
        return (f"{self.__class__.__name__} (id={self.id},"
                f"{self.product_name},"
                f"{self.product_description},"
                f"{self.product_price})")

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'product_img': self.product_img,
            'product_description': self.product_description,
            'product_sizes': self.product_sizes,
            'product_price': self.product_price,
            'category_id': self.category_id,
        }

