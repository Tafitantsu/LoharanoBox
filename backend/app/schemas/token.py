from pydantic import BaseModel
from typing import Optional
import uuid

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    id: Optional[uuid.UUID] = None
    exp: Optional[int] = None
