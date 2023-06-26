from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession

from .settings import settings


DB_USER: str = settings.database.DB_USER
DB_PASS: str = settings.database.DB_PASS
DB_PORT: int = settings.database.DB_PORT
DB_HOST: str = settings.database.DB_HOST
DB_NAME: str = settings.database.DB_NAME

DATABASE_URL: str = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL)
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
