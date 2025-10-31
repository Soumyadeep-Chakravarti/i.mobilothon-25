# backend/app/src/services/user.py
import logging
from typing import Optional

from beanie import PydanticObjectId
from db.models import User
from utils import hash_password

logger = logging.getLogger(__name__)


class UserService:
    """
    Handles profile management and data personalization.
    Manages CRUD for User documents in MongoDB.
    """

    async def create_user(self, email: str, password: str, username: str) -> User:
        """
        Registers a new user, hashing the password before persistence.
        """
        if await User.find_one(User.email == email):
            raise ValueError("Email already registered.")

        hashed_pwd = hash_password(password)

        user = User(email=email, username=username, hashed_password=hashed_pwd)

        # Data persisted or retrieved from MongoDB (async)
        await user.insert()
        return user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Fast query retrieval using indexed collections."""
        return await User.find_one(User.email == email)

    async def get_user_by_id(self, user_id: PydanticObjectId) -> Optional[User]:
        """Retrieves a user by their MongoDB object ID."""
        return await User.get(user_id)

    async def update_user_preferences(
        self, user_id: PydanticObjectId, updates: dict
    ) -> Optional[User]:
        """Updates embedded preferences document."""
        user = await self.get_user_by_id(user_id)
        if user:
            # Simple update for demonstration
            user.preferences.update(updates)
            await user.save()
            return user
        return None


user_service = UserService()
