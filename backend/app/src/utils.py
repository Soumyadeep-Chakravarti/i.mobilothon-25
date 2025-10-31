# backend/app/src/utils.py
from datetime import datetime, timedelta
from typing import Optional

import jwt
from core.config import settings
from passlib.context import CryptContext

# Password Hashing Context (Argon2/Bcrypt)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashes a password for secure storage."""
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a stored hash."""
    return password_context.verify(password, hashed_password)


# --- JWT Utility Functions (Stateless Authentication) ---


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Creates a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default expiry, e.g., 30 minutes
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# NOTE: A function for token decoding/validation would be added here later for middleware.
