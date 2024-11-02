from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.responses import JSONResponse
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


@app.get("/users/{user_email}",tags=["users"],response_model=UserResponse)
async def get_user_by_email(user_email:str,db:AsyncSession = Depends(get_db)):
  
  user_db = await crud.get_user_by_email(user_email,db)
  
  if not user_db:
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="User not found")
  
  data = UserResponse.from_orm(user_db).model_dump()
  
  return JSONResponse(content = data, status_code = status.HTTP_200_OK)


@app.post("/users", tags=["users"],response_model=UserResponse)
async def create_user(user:UserCreate,db:AsyncSession = Depends(get_db)):
  
  user_create = await crud.create_user(user,db)
  
  if user_create is None:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The username or email already exists")

  data = UserResponse.from_orm(user_create).model_dump()
   
  return JSONResponse(content = {"messages":"Created successfully",
                                 "data":data
                                 },status_code = status.HTTP_201_CREATED)


@app.patch("/users/{user_name}",tags=["users"],response_model=UserResponse)
async def update_user(user_name,is_active:bool,db:AsyncSession = Depends(get_db)):
  
  user_update = await crud.update_user(user_name,is_active,db)
  
  if not user_update:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
  
  data = UserResponse.from_orm(user_update).model_dump()
  
  return JSONResponse(content = data, status_code=status.HTTP_200_OK)

@app.delete("/users/{user_id}",tags=["users"], response_model=dict)
async def delete_user(user_id:int,db:AsyncSession = Depends(get_db)):
  
  results = await crud.delete_user(user_id,db)
  
  if not results:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or already deleted ")
  
  return JSONResponse(content=results,status_code=status.HTTP_200_OK)