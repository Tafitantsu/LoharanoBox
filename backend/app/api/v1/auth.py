from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.schemas.auth import UserLogin, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService
from app.db.session import get_db
from app.schemas.auth import TokenPayload
from app.core.jwt import decode_access_token

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(db)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        user = auth_service.register_user(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/login", response_model=Token)
def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        token = auth_service.authenticate_user(
            credentials.username, credentials.password
        )
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    pass

@router.get("/me", response_model=UserResponse)
def get_current_user(
    user: TokenPayload = Depends(decode_access_token),
    auth_service: AuthService = Depends(get_auth_service),

):
    current_user = auth_service.fetch_user_by_username(user.sub)

    
    return current_user