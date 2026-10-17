from pydantic import BaseModel, Field, ConfigDict, field_serializer, EmailStr


class UserCreateSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    password: str

class GetUserSchema(BaseModel):
    id: int 
    username: str
    email: EmailStr
    model_config =ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    access_token: str 
    token_type: str = "bearer"
    