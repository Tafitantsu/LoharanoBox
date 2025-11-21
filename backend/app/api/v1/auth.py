from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.auth import Token
from app.services.auth_service import AuthService
from app.db.session import get_db
router = APIRouter()


@router.post("/token", response_model=Token)
def login(
    form_data : OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        auth_service = AuthService(db)
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