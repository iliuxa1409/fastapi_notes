from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from auth import create_access_token, hash_password, verify_password, get_current_user
import models
import schemas
from database import get_db

router = APIRouter()

# Схема для извлечения токена из запроса
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Создание пользователя
@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


# Аутентификация пользователя
@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User).filter(models.User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Защищенный маршрут
@router.get("/users/me", response_model=schemas.User)
async def read_users_me(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    token_data = get_current_user(token)
    result = await db.execute(select(models.User).filter(models.User.username == token_data.username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user
