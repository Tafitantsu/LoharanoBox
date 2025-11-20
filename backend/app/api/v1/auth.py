from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import UserLogin, Token
from app.services.auth_service import AuthService
router = APIRouter()


@router.post("/token", response_model=Token)
def login(
    form_data : OAuth2PasswordRequestForm = Depends()
):
    try:
        auth_service = AuthService()
        token = auth_service.authenticate_user(email=form_data.username, password=form_data.password)
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    
@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    pass