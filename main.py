from fastapi import FastAPI
from create_db import life_span


app = FastAPI(
  title = "Login",
  docs_url = "/",
  description = "This is a app of login",
  lifespan = life_span
)

@app.get("/users")
async def get_all_users():
  return {"message":"Todos los usuarios"}


@app.get("/users/{user_id}")
async def get_user_by_id(user_id:int):
  return {"message":"usuario por id"}


@app.post("/users")
async def create_user():
  return {"message":"usuario creado"}


@app.put("/users/{user_id}")
async def create_user(usr_id:int):
  return {"message":"Usuario actualizado"}


@app.delete("/users/{user_id}")
async def get_all_users(user_id:int):
  return {"message":"usuario eliminado"}