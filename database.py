from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'postgresql://user:password@localhost:5432/mydatabase'

# Синхронный движок и сессия для Flask
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Асинхронный движок и сессия для бота
async_engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Создание таблиц для синхронного движка
Base.metadata.create_all(bind=engine)


# Получение синхронной сессии
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Получение асинхронной сессии
async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        yield session


# Асинхронная функция для создания таблиц с асинхронным движком
async def create_async_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
