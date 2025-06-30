from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .cart import Cart

class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    username: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default="user")
    cart: Mapped[list["Cart"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    cart_items = relationship("Cart", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")