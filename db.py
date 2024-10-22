from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
from typing import AsyncGenerator
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

BASE =declarative_base()

engine = create_async_engine(DATABASE_URL)

async_session_local = async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False
)

async def get_db()->AsyncGenerator[AsyncSession,None]:
  async with async_session_local() as session:
    try:
      yield session
    finally:
      await session.close()