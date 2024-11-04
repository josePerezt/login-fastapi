# importar el modelo
from models import User
# importamos la session
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserCreate,UserResponse
from sqlalchemy import select, delete, update
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
  
  async def update_user(self,user_name,is_active,db:AsyncSession):
    
    # Se busca el usuario y se valida su existencia en la DB
    query = await db.execute(select(User).where(User.name == user_name))

    data_user = query.scalar_one_or_none()
    
    # si no se obtinee resultado se retorna NONE
    if not data_user:
      return None
    
    # si el usuario existe se actualiza
    else:
      query_update = update(User).where(User.name == user_name).values(is_active = is_active)
    
      await db.execute(query_update)
      await db.commit()
      
    # se retorn ael usuario actualizado
    user_update = await db.execute(select(User).where(User.name == user_name))
  
    return user_update.scalar_one()
    
  async def delete_user(self,user_id, db:AsyncSession):
    
    query = delete(User).where(User.id == user_id).returning(User.name)
    
    results = await db.execute(query)
    
    print(results.scalar())
    
    if not results.scalar():
      return None
    
    await db.commit()
    return {"message":F"User '{User.name}' deleted successfully"}
  
  async def get_user_by_name(self,form_data,db:AsyncSession):
    
    query = select(User).filter(User.name == form_data.username)
    
    user_db = await db.execute(query)
    
    user_response = user_db.scalar_one_or_none()
    
    return user_response
  
    
    
    
    
  
  