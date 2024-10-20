from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = 'postgresql://user:password@localhost:5432/mydatabase'

# Synchronous engine and session for Flask
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine and session for bot
async_engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


# Create tables with the synchronous engine
Base.metadata.create_all(bind=engine)


# Synchronous session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Asynchronous session
async def get_async_db_session():
    async with AsyncSessionLocal() as session:
        yield session


# Asynchronous function to create tables with the async engine
async def create_async_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
