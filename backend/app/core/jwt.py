from datetime import datetime, timedelta
from typing import Any, Optional

from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException

from app.core.config import settings
from app.schemas.auth import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """
    Generate a JWT access token.

    :param data: Payload data (e.g., {"sub": username}).
    :param expires_delta: Token validity duration. Defaults to settings.ACCESS_TOKEN_EXPIRE_MINUTES.
    :return: Encoded JWT string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Decode and validate a JWT access token.

    :param token: JWT token.
    :return: TokenPayload containing `sub` and `exp`.
    :raises JWTError: if token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        id: Optional[str] = payload.get("id")
        username: Optional[str] = payload.get("sub")
        exp: Optional[int] = payload.get("exp")
        if username is None or exp is None:
            raise JWTError("Invalid token payload")
        if id is None:
            raise JWTError("Invalid token payload")
        if exp is None:
            raise JWTError("Invalid token payload")
        
        return TokenPayload(id=id, sub=username, exp=exp)
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {e}") 
