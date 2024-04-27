from pydantic import BaseModel
from typing import Optional


# Схема для входных данных пользователя
class UserBase(BaseModel):
    username: str
    email: str
    password: str


# Схема для создания пользователя
class UserCreate(UserBase):
    pass


# Схема для обновления пользователя
class UserUpdate(UserBase):
    pass


# Схема для возвращаемых данных пользователя
class User(UserBase):
    id: int

    class Config:
        orm_mode = True
