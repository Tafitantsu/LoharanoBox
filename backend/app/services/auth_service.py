from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password
from app.core.jwt import create_access_token

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def authenticate_user(self, username: str, password: str) -> str:
        user = self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid username or password")
        user.id = str(user.id)
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"id": user.id, "sub": user.username}, expires_delta=access_token_expires
        )
        return access_token
