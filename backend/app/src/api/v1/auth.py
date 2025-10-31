# backend/app/src/api/v1/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.auth import auth_service
from services.user import user_service

router = APIRouter()


# Pydantic models for API request/response
class UserRegistration(BaseModel):
    email: EmailStr
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


@router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserRegistration):
    """Endpoint for user registration."""
    try:
        new_user = await user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            username=user_data.username,
        )
        return auth_service.create_user_tokens(new_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login_user(
    form_data: UserRegistration,
):  # Using same schema for email/password input
    """Endpoint for user login."""
    user = await auth_service.authenticate_user(
        email=form_data.email, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return auth_service.create_user_tokens(user)
