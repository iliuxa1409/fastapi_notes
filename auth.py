from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
import models
from schemas import TokenData


# Секретный ключ для шифрования JWT
SECRET_KEY = "2fcb1544cbaf55b171b9e87ddcd434d178270cdda1aef1ffc4ad6775868e1455"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Настройка контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хэширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# Проверка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Создание JWT токена
def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Получение текущего пользователя
def get_current_user(token: str):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f'Decoded username: {username}') # Логирование
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


# Получение текущего активного пользователя
async def get_current_active_user(current_user: models.User =
                                  Depends(get_current_user)):
    return current_user
