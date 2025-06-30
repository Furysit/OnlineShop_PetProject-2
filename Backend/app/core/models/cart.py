from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base

class Cart(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"),nullable=True)
    quantity: Mapped[int] = mapped_column(default=1, nullable=True)

    user = relationship("User", back_populates = "cart_items")
    product = relationship("Product", back_populates= "carts")
