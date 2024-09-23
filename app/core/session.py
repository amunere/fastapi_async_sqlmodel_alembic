from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

async_engine = create_async_engine(
   url=settings.ASYNC_DATABASE_URI.unicode_string(),
   echo=True,
   future=True
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)