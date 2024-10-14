
from db import engine,BASE
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Funcion que crea la base de datos
async def create_db():
  async with engine.begin() as conn:
    from models import User
    
    await conn.run_sync(BASE.metadata.drop_all)
    await conn.run_sync(BASE.metadata.create_all)
  
  await engine.dispose()
  
# funcion que crea la base de datos CUANDO se inicia la app
@asynccontextmanager
async def life_span(app:FastAPI):
  await create_db()
  yield