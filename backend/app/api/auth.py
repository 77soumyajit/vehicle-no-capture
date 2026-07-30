from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    return AuthService.register(
        db,
        request,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    result = AuthService.login(
        db,
        request.username,
        request.password,
    )

    return {
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": result["token_type"],
    }