from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from datetime import datetime



class ProductShort(BaseModel):
    id: int
    name: str
    price: int
    model_config = ConfigDict(from_attributes=True)


class OrderItem(BaseModel):
    id: int
    quantity: int
    product: Optional[ProductShort]  
    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    user_id: int
    total_price: int
    

class Order(OrderBase):
    id: int
    order_items: list[OrderItem]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)