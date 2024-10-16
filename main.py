from fastapi import FastAPI,Depends,HTTPException
# from create_db import life_span
from schemas import UserResponse,UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from crud import CRUD

crud = CRUD()




app = FastAPI(
  title = "Login",
  docs_url = "/",
  description = "This is a app of login",
  # lifespan = life_span
)

@app.get("/users",tags=["users"], response_model = list[UserResponse])
async def get_all_users(db:AsyncSession = Depends(get_db)):
  
  db_users = await crud.get_all_users(db)
  
  if not db_users:
    raise HTTPException(status_code=404, detail="there are no registered users")
  
  return db_users


@app.get("/users/{user_id}")
async def get_user_by_id(user_id:int):
  return {"message":"usuario por id"}


@app.post("/users", tags=["users"],response_model = dict)
async def create_user(user:UserCreate,db:AsyncSession = Depends(get_db)):
  
  query = await crud.create_user(db,user)
  
  print(query)
  
  return {"message":"usuario creado"}


@app.put("/users/{user_id}")
async def create_user(usr_id:int):
  return {"message":"Usuario actualizado"}


@app.delete("/users/{user_id}")
async def get_all_users(user_id:int):
  return {"message":"usuario eliminado"}