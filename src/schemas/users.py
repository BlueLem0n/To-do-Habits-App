from pydantic import BaseModel, Field, ConfigDict, field_serializer, EmailStr


class UserCreateSchema(BaseModel):
    username: str 
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class GetUserSchema(BaseModel):
    id: int 
    username: str
    email: EmailStr
    model_config =ConfigDict(from_attributes=True)

class TokenSchema(BaseModel):
    access_token: str 
    token_type: str = "bearer"
    