# backend/app/src/api/v1/data.py (NEW FILE)
from typing import Any, Dict, List

from db.models import (
    PydanticObjectId,
)  # Use this type for MongoDB IDs in Pydantic models
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from services.data import data_service

router = APIRouter()


# --- Pydantic Models ---
class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=120)
    details: Dict[str, Any] = Field(
        default={}, description="Flexible JSON object for project metadata."
    )


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    owner_id: PydanticObjectId
    name: str
    status: str
    details: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {PydanticObjectId: str}


# -----------------------


# Dependency Placeholder for the Authenticated User (Simulating JWT Auth)
def get_current_user_id() -> PydanticObjectId:
    """Placeholder: In production, this extracts the user ID from the JWT."""
    # Hardcoded ID for demonstration linked to the user.py placeholder
    return PydanticObjectId("ffffffffffffffffffffffff")


@router.post(
    "/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED
)
async def create_new_project(
    project_data: ProjectCreate,
    owner_id: PydanticObjectId = Depends(get_current_user_id),
):
    """Creates a new project entity."""
    project = await data_service.create_project(
        owner_id=owner_id, name=project_data.name, details=project_data.details
    )
    return project


@router.get("/projects", response_model=List[ProjectResponse])
async def list_user_projects(owner_id: PydanticObjectId = Depends(get_current_user_id)):
    """Retrieves all projects owned by the current user."""
    return await data_service.get_projects_by_owner(owner_id)


@router.patch("/projects/{project_id}", response_model=ProjectResponse)
async def update_project_details(
    project_id: PydanticObjectId,
    updates: ProjectUpdate,
    owner_id: PydanticObjectId = Depends(get_current_user_id),
):
    """Updates the details of a specific project."""
    updated_project = await data_service.update_project(
        project_id=project_id,
        owner_id=owner_id,
        updates=updates.model_dump(exclude_none=True),
    )
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied.",
        )
    return updated_project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_entity(
    project_id: PydanticObjectId,
    owner_id: PydanticObjectId = Depends(get_current_user_id),
):
    """Deletes a project."""
    success = await data_service.delete_project(project_id, owner_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied.",
        )
    return
