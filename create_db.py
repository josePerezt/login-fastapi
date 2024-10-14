
from db import engine,BASE


async def create_db():
  async with engine.begin() as conn:
    from models import User
    
    await conn.run_sync(BASE.metadata.drop_all)
    await conn.run_sync(BASE.metadata.create_all)
  
  await engine.dispose()