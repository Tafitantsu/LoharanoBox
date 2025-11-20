from uuid import UUID
from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="strongpassword123")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    id : UUID
    sub: str
    exp: int
