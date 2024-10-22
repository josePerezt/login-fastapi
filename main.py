from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import JSONResponse
from schemas import UserResponse,UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from crud import CRUD
from utils.serializer import model_serializer
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


@app.get("/users/{user_email}",tags=["users"],response_model=UserResponse)
async def get_user_by_email(user_email:str,db:AsyncSession = Depends(get_db)):
  
  user_db = await crud.get_user_by_email(user_email,db)
  
  # serializamos el modelo para retornarlo como json
  user_serializer = model_serializer(user_db)
  
  if not user_db:
    raise HTTPException(status_code=404, detail="User not found")
  
  return JSONResponse(content=user_serializer, status_code=200)


@app.post("/users", tags=["users"],response_model=UserResponse)
async def create_user(user:UserCreate,db:AsyncSession = Depends(get_db)):
  
  query_user_create = await crud.create_user(user,db)
  
  user_create = model_serializer(query_user_create)
  
  if query_user_create is None:
    raise HTTPException(status_code=400, detail="The username or email already exists")
  
  
  return JSONResponse(content = {"messages":"Created successfully",
                                 "data":user_create
                                 },status_code = 200)


@app.put("/users/{user_email}",tags=["users"])
async def upadte_user():
    pass


@app.delete("/users/{user_id}",tags=["users"])
async def get_all_users(user_id:int):
  return {"message":"usuario eliminado"}