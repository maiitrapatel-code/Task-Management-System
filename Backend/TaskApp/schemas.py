from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class TaskRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr  # Validates email format
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str