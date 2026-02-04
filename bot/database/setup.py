from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.database.models import Base
import os

# SQLite faylga yozamiz (serverda PostgreSQL ga o'zgaradi)
DB_URL = "sqlite+aiosqlite:///bot.db"

engine = create_async_engine(DB_URL, echo=False)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """Bazani va jadvallarni yaratish"""
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Test uchun (kerak bo'lsa)
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncSession:
    """Session olish uchun generator"""
    async with async_session_maker() as session:
        yield session
