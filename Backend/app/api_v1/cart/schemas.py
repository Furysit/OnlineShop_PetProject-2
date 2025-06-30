from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from app.api_v1.products.schemas import Product

class CartBase(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class CartAddRequest(BaseModel):
    product_id: int
    quantity: int = 1

class Cart(CartBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True) 

class Cart_ext(CartBase):
    id: int
    user_id: int
    product: Product
    model_config = ConfigDict(from_attributes=True)