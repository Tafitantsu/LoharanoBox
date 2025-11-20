from fastapi import Depends, HTTPException, status
from typing import List
from passlib.context import CryptContext
from app.dependencies import get_current_active_user
from app.models.user import User as UserModel

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

class PermissionChecker:
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions

    def __call__(self, current_user: UserModel = Depends(get_current_active_user)) -> bool:
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no role assigned."
            )

        user_permissions = {p.nom for p in current_user.role.permissions}

        if not all(req_perm in user_permissions for req_perm in self.required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges."
            )
        return True