from sqlalchemy.orm import Mapped, mapped_column, relationship 
from sqlalchemy import ForeignKey, DateTime
from datetime import datetime, timezone
from .base import Base

class Order(Base):
    user_id : Mapped[int] = mapped_column(ForeignKey("user.id"))
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),default= lambda: datetime.now(timezone.utc))
    total_price: Mapped[int] = mapped_column()

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    user = relationship("User", back_populates="orders")