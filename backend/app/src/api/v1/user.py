# backend/app/src/api/v1/user.py
from beanie import PydanticObjectId  # To handle MongoDB IDs
from db.models import User
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from services.user import user_service

router = APIRouter()


class UserProfile(BaseModel):
    id: PydanticObjectId
    email: EmailStr
    username: str
    preferences: dict
    is_active: bool

    # Configuration to handle MongoDB's default `_id` field
    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    theme: str
    notifications: bool


@router.get("/me", response_model=UserProfile)
async def get_current_user():
    """Retrieves the profile of the currently authenticated user (placeholder)."""
    # NOTE: In a complete implementation, this user ID would come from JWT validation.

    # Hardcoded ID for demonstration (Replace with actual JWT dependency)
    placeholder_user_id = PydanticObjectId("ffffffffffffffffffffffff")

    user = await user_service.get_user_by_id(placeholder_user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.patch("/me/preferences", response_model=UserProfile)
async def update_user_preferences(prefs: UserPreferencesUpdate):
    """Updates preferences for the current user."""
    # Hardcoded ID for demonstration
    placeholder_user_id = PydanticObjectId("ffffffffffffffffffffffff")

    updated_user = await user_service.update_user_preferences(
        placeholder_user_id, updates=prefs.model_dump()
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return updated_user
