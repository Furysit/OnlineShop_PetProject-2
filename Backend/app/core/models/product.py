from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, Optional
from .base import Base

if TYPE_CHECKING:
    from .category import Category


class Product(Base):
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    category_id : Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    category : Mapped["Category"] = relationship(back_populates="products")
    image_url: Mapped[Optional[str]] = mapped_column(nullable=True) 
    carts = relationship("Cart", back_populates="product")
    orders = relationship("OrderItem", back_populates="product")