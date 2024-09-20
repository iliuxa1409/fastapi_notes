from sqlalchemy.orm import Session
from . import models, schemas


# Получение всех заметок
def get_notes(db: Session, skip: int = 0,  limit: int = 10):
    return db.query(models.Note).offset(skip).limit(limit).all()

# Создание новой заметки
