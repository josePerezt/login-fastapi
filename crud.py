# importar el modelo
from models import User
# importamos la session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate
from sqlalchemy import select
from AUTH.pwd_bcrypt import generate_password_hash


class CRUD:
  
  async def get_all_users(self,db:AsyncSession):
    query = select(User)
    
    users = await db.execute(query)
    
    if not users:
      return []
    return users.scalars().all()    
  
  async def create_user(self,user:UserCreate,db:AsyncSession):
    # Le pasamos los datos para el registro al modelo
    
    hashed_pass = (generate_password_hash(user.password))
    
    user_data= User(name = user.name, email=user.email, password =  hashed_pass)
  
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
  
  async def get_user_by_email(self,email:str,db:AsyncSession):
    
    query = select(User).filter_by(email=email)
    
    user = await db.execute(query)
    
    if not user:
      return None
    
    user_data = user.scalars().first()
    
    return user_data