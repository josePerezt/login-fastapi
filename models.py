from db import BASE
from sqlalchemy import String,Integer,Boolean
from sqlalchemy.orm import Mapped,mapped_column


class User(BASE):
  __tablename__ ="users"
  
  id: Mapped[int] = mapped_column(Integer,primary_key=True)
  name: Mapped[str] = mapped_column(String(30),nullable=False,unique=True)
  email:Mapped[str] = mapped_column(String(200),nullable=False,unique=True)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  code_password: Mapped[int] = mapped_column(Integer)
  is_active : Mapped[bool] = mapped_column(Boolean,default=True)
  
  def __str__(self):
    return f"Name: {self.name}, email: {self.email}"
  