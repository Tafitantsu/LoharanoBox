from datetime import timedelta
from sqlalchemy.orm import Session
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import verify_password, get_password_hash
from app.core.jwt import create_access_token
from app.models.user import User

class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register_user(self, user_data: UserCreate) -> User:
        if self.repo.get_by_username(user_data.username):
            raise ValueError("Username already exists")
        if self.repo.get_by_email(user_data.email):
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_data.password)
        user = self.repo.create(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )
        return user

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
    def fetch_user_by_username(self, username: str) -> str:
        user = self.repo.get_by_username(username)
        if not user:
            raise ValueError("Invalid username")

        return user
