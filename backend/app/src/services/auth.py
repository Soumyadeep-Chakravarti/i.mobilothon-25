# backend/app/src/services/auth.py
from datetime import timedelta
from typing import Optional

from core.config import settings
from db.models import User
from services.user import user_service
from utils import create_access_token, verify_password

# Token expiry (e.g., 60 minutes for Access Token)
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthService:
    """
    Manages registration, login, and token lifecycle.
    JWT-based, stateless authentication.
    """

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Validates user credentials against the database.
        """
        user = await user_service.get_user_by_email(email)

        if not user or not user.is_active:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def create_user_tokens(self, user: User) -> dict:
        """
        Generates access and refresh tokens for a successful login.
        """
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": str(user.id)},  # Use MongoDB ID as the subject
            expires_delta=access_token_expires,
        )

        # Refresh token logic would be more complex and implemented later

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # seconds
        }


auth_service = AuthService()
