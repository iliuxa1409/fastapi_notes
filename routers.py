from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import models
import schemas
from database import get_db

router = APIRouter()


@router.post("/notes/", response_model=schemas.Note)
async def create_note(note: schemas.NoteCreate, db: AsyncSession = Depends(
    get_db)):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


@router.get("/notes/", response_model=list[schemas.Note])
async def read_notes(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note).offset(skip).limit(limit))
    notes = result.scalars().all()
    return notes


@router.get("/notes/{note_id}", response_model=schemas.Note)
async def read_note(note_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Note).where(models.Note.id == note_id))
    note = result.scalars().first()
    if note in None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/notes/{note_id}", response_model=schemas.Note)
async def update_note(note_id: int, note: schemas.NoteCreate,
                db: AsyncSession = Depends(get_db)):
    db_note = await read_note(note_id, db)
    for key, value in note.dict().items():
        setattr(db_note, key, value)
    await db.commit()
    await db.refresh(db_note)
    return db_note


@router.delete("/notes/{note_id}", response_model=schemas.Note)
async def delete_note(note_id: int, db: AsyncSession = Depends(get_db)):
    db_note = await  read_note(note_id, db)
    await db.delete(db_note)
    await db.commit()
    return db_note
