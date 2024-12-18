from pydantic import BaseModel,Field

class UserBase(BaseModel):
  name:str = Field(min_length = 5, max_length = 15 )
  email: str = Field(min_length = 10, max_length = 30)
  
class UserCreate(UserBase):
  password: str = Field(...,min_length = 8, max_length = 16)
  
class UserUpdateActive(BaseModel):
  is_active: bool 
  
class UserResponse(UserBase):
  id : int
  is_active : bool
  
  class Config:
    orm_mode=True
    from_attributes=True