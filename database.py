from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL для подключения к базе данных PostgreSQL
DATABASE_URL = "postgresql+asyncpg://myuser:mysecurepassword@localhost" \
               "/mydatabase"

# Создаем асинхронный движок для работы с БД
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,
                       class_=AsyncSession)

# Базовый класс для всех моделей
Base = declarative_base()


# функция для получения сессии БД
async def get_db():
    async with SessionLocal() as session:
        yield session
