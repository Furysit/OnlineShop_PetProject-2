from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional

# schemas/user.py

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=20)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role: str = Field(default="user", min_length=4)

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "username": "johndoe",
                "password": "strongpassword",
                "role": "user"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "strongpassword"
            }
        }

class UserOut(UserBase):
    id: int
    role: str

    model_config = ConfigDict(from_attributes=True)

class UserInToken(BaseModel):
    id: int
    email: EmailStr
    role: str

class TokenWithUser(BaseModel):
    access_token: str
    token_type: str
    user: UserInToken

class LoginRequest(BaseModel):
    email: str
    password: str