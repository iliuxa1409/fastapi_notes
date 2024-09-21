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


# Схема для пользователя
class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
