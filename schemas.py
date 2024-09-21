from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# Базовая схема для заметок
class NoteBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []


# Схема для создания заметок
class NoteCreate(NoteBase):
    pass


# Схема для отображения заметки
class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Схема для создания пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Схема для отображения пользователя
class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        orm_mode = True


# Схема для токена
class Token(BaseModel):
    access_token: str
    token_type: str


# Данные для токена
class TokenData(BaseModel):
    username: Optional[str] = None
