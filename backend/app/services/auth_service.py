from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import RegisterRequest
from app.services.jwt_service import JWTService


class AuthService:
    """
    Service class for handling authentication-related operations.
    """

    @staticmethod
    def register(
        db: Session,
        request: RegisterRequest,
    ):
        existing_user = UserRepository.get_by_username(
            db,
            request.username,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists.",
            )

        existing_email = UserRepository.get_by_email(
            db,
            request.email,
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists.",
            )

        user = User(
            username=request.username,
            email=request.email,
            full_name=request.full_name,
            hashed_password=hash_password(
                request.password
            ),
            role=request.role,
        )

        return UserRepository.create(
            db,
            user,
        )

    @staticmethod
    def login(
        db: Session,
        username: str,
        password: str,
    ):
        user = UserRepository.get_by_username(
            db,
            username,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        payload = {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id,
        }

        access_token = JWTService.create_access_token(
            payload
        )

        refresh_token = JWTService.create_refresh_token(
            payload
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str,
    ):
        """
        Validate refresh token and generate
        a brand-new access token.
        """

        payload = JWTService.verify_refresh_token(
            refresh_token
        )

        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        user = UserRepository.get_by_id(
            db,
            payload["user_id"],
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found.",
            )

        new_payload = {
            "sub": user.username,
            "role": user.role,
            "user_id": user.id,
        }

        access_token = JWTService.create_access_token(
            new_payload
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }