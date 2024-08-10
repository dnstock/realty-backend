from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class ItemBase(BaseModel):
    title: str
    description: str

class ItemCreate(ItemBase):
    category_id: int

class Item(ItemBase):
    id: int
    owner_id: int
    category_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attributes: True
