from pydantic import BaseModel, EmailStr, Field
from .models import UserRole
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    role: UserRole = Field(default=UserRole.reader)

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int]=None

class PostCreate(BaseModel):
    title: str
    content: str
