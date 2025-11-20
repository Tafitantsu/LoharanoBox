from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(..., example="johndoe@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, example="strongpassword123")

class UserResponse(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
