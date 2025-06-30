
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional



class CategoryBase(BaseModel):
    name : str
    
class CategoryCreate(CategoryBase):
    pass
class CategoryOut(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
class Category(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str = Field(..., min_length=2)
    description: str
    price: int = Field(..., gt=0 )
    category_id: int | None = None
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductCreate):
    pass

class ProductPartialUpdate(ProductBase):
    name: str | None = None
    description: str| None = None
    price: int| None = None
    category_id: int | None = None

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int