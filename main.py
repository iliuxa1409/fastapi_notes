from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas
from .database import SessionLocal, get_db

app = FastAPI()


@app.post("/notes", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(
    get_db)):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


@app.get("/notes/{note_id}", response_model=schemas.Note)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note).filter(models.Note.id ==
    note_id))
    note = result.scalars().first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
