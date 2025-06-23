from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas import auth as auth_schemas
from app.schemas import user as user_schemas
from app.models.user import User
from app.crud import user as user_crud

router = APIRouter()

@router.post("/auth/register", response_model=user_schemas.User)
def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: user_schemas.UserCreate,
) -> Any:
    """
    Register a new user.
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this username already exists.",
        )
    user = user_crud.create(db, obj_in=user_in)
    return user

@router.post("/auth/login", response_model=auth_schemas.Token)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    return {
        "access_token": security.create_access_token(
            user.username, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(
            user.username, expires_delta=refresh_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/auth/refresh", response_model=auth_schemas.Token)
def refresh_token(
    *,
    db: Session = Depends(deps.get_db),
    refresh_token: auth_schemas.RefreshToken,
) -> Any:
    """
    Refresh access token using refresh token.
    """
    username = security.verify_token(refresh_token.refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user_crud.get_by_username(db, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    return {
        "access_token": security.create_access_token(
            user.username, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(
            user.username, expires_delta=new_refresh_token_expires
        ),
        "token_type": "bearer",
    } 