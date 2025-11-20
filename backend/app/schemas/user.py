import uuid
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

# Permission Schemas
class PermissionBase(BaseModel):
    nom: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    pass

class PermissionInDB(PermissionBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID

# Role Schemas
class RoleBase(BaseModel):
    nom: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleInDB(RoleBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    permissions: List[PermissionInDB] = []

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    mot_de_passe: str
    role_id: uuid.UUID

class UserRegister(UserBase):
    mot_de_passe: str

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = None
    role_id: Optional[uuid.UUID] = None
    actif: Optional[bool] = None

class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    date_creation: datetime
    role: Optional[RoleInDB] = None

class UserManage(UserInDB):
    actif: bool