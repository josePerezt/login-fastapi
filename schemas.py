from pydantic import BaseModel,Field
from typing import Optional

class UserBase(BaseModel):
  name:str = Field(min_length = 5, max_length = 15 )
  email: str = Field(min_length = 10, max_length = 30)
  
class UserCreate(UserBase):
  password: str = Field(...,min_length = 8, max_length = 16)
  
class UserUpdatePassword(BaseModel):
  password: str = Field(...,min_length=8)
  new_password: str= Field(...,min_length=8)
  
  
class UserResponse(UserBase):
  id : int
  is_active : bool
  
  class config:
    orm_mode : True