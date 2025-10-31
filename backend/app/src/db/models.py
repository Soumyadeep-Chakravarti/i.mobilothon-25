# backend/app/src/db/models.py
from datetime import datetime
from typing import Optional

from beanie import Document
from db.client import DOCUMENT_MODELS  # Import the list to register models
from pydantic import EmailStr, Field


# --- User Domain Model ---
class User(Document):
    """
    Stores complete user profiles with embedded preferences and metadata.
    Implements Denormalization by embedding metadata.
    """

    email: EmailStr = Field(unique=True, index=True)
    username: Optional[str] = Field(unique=True, index=True)
    hashed_password: str

    # Embedded document for Preferences (Denormalization)
    preferences: dict = Field(default={"theme": "dark", "notifications": True})

    # Metadata fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True

    # Custom Settings for MongoDB/Beanie
    class Settings:
        name = "users"  # MongoDB collection name
        # Define compound indexes for search-heavy collections (Indexing Strategy)
        indexes = [("email", "username")]


# Register the model with the client list
DOCUMENT_MODELS.append(User)


class Project(Document):
    """
    Stores project-specific entities. Features schema flexibility for project details.
    """

    owner_id: PydanticObjectId  # Link back to the User who owns the project
    name: str = Field(index=True)
    status: str = Field(default="Draft")

    # Flexible field to store semi-structured data
    details: Dict[str, Any] = Field(default={})

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Custom Settings for MongoDB/Beanie
    class Settings:
        name = "projects"  # MongoDB collection name
        # Compound index for efficient queries (e.g., finding a user's projects by status)
        indexes = [("owner_id", "status", "created_at")]


# Register the new model
DOCUMENT_MODELS.append(Project)
