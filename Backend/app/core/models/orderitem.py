from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey

from .base import Base

class OrderItem(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id : Mapped[int] = mapped_column(ForeignKey("product.id",ondelete="SET NULL"), nullable=True)
    quantity: Mapped[int] = mapped_column()

    product = relationship("Product", back_populates="orders",passive_deletes=True)
    order = relationship("Order", back_populates="order_items")