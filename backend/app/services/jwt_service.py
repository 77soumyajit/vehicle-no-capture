from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

from app.core.config import settings


class JWTService:

    @staticmethod
    def create_access_token(data: dict):

        payload = data.copy()

        payload["type"] = "access"

        payload["exp"] = (
            datetime.now(timezone.utc)
            + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def create_refresh_token(data: dict):

        payload = data.copy()

        payload["type"] = "refresh"

        payload["exp"] = (
            datetime.now(timezone.utc)
            + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str):

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            return payload

        except JWTError:
            return None