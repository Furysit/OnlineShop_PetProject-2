from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .product import Product

class Category(Base):
    name: Mapped[str] = mapped_column()
    products: Mapped[list["Product"]] = relationship(back_populates="category") 