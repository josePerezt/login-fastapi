# importar el modelo
from models import User
# importamos la session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate
from sqlalchemy import select


class CRUD:
  
  async def get_all_users(self,db:AsyncSession):
    query = select(User)
    
    users = await db.execute(query)
    
    if not users:
      return []
    return users.scalars().all()    
  
  async def create_user(self,user:UserCreate,db:AsyncSession):
    # Le pasamos los datos para el registro al modelo
    user_data= User(name = user.name, email=user.email, password = user.password)
  
    # validamos que no exista ni el name ni el email del usuario.
    existing_user = await db.execute(select(User).filter((User.name == user.name) | (User.email == user.email)))
    
    existing = existing_user.scalars().first()   
    
    # Si existe retornamos None y si no existe lo creamos
    if existing:
      print("existe el usuario")
      return None

    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    
    return user_data