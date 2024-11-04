import bcrypt

def generate_password_hash(password:str):
  
  my_pass = password.encode("utf-8")
  
  hashed = bcrypt.hashpw(my_pass,bcrypt.gensalt(10))
  
  pwd = hashed.decode("utf-8")

  return pwd

def check_password(password:str,password_db:str):
  
  password = password.encode("utf-8")
  password_db = password_db.encode("utf-8")
  
  verify = bcrypt.checkpw(password,password_db)
  
  if verify:
    return True
  return False