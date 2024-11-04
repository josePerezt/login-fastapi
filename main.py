from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from schemas import UserResponse,UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from dotenv import load_dotenv
import os
from AUTH.pwd_bcrypt import check_password
from jose import jwt
from db import get_db
from crud import CRUD

crud = CRUD()

load_dotenv()

jwt_secret_key = os.getenv("MY_SECRET_KEY")
jwt_algorithm = os.getenv("ALGORITHM")

app = FastAPI(
  title = "Login",
  docs_url = "/",
  description = "This is a app of login",
  # lifespan = life_span
)

# AUTH

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def encode_token(payload:dict)->str:
  token = jwt.encode(payload,key=jwt_secret_key,algorithm=jwt_algorithm)
  return token

def decode_token(token:Annotated[str, Depends(oauth_scheme)])->dict:
  
  user = jwt.decode(token=token,key=jwt_secret_key,algorithms=jwt_algorithm)
  return user


@app.post("/token",tags=["AUTH"])
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:AsyncSession = Depends(get_db)):
  
  user_db = await crud.get_user_by_name(form_data,db)
  
  password = check_password(form_data.password,user_db.password)
  print(password)
  
  if not user_db:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect username")
  elif not password:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
  
  user_data = UserResponse.from_orm(user_db).model_dump()
  
  token = encode_token(user_data)
  
  return {"access_token":token,"token_type":"bearer"}

@app.get("/users/profile", tags=["AUTH"])
async def profile(my_user:Annotated[dict, Depends(decode_token)]):
  return my_user

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