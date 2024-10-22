from schemas import UserResponse
def model_serializer(models):
  user = UserResponse(
    id= models.id,
    name= models.name,
    email= models.email,
    is_active = models.is_active
  ).model_dump()
  
  return user