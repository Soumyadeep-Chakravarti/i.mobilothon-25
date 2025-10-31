# backend/app/src/services/data.py (UPDATED)
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from db.models import Project, PydanticObjectId

logger = logging.getLogger(__name__)


class DataService:
    """
    Manages CRUD for project-specific entities (e.g., Projects, Documents).
    """

    # --- Project Management CRUD ---

    async def create_project(
        self, owner_id: PydanticObjectId, name: str, details: Dict[str, Any]
    ) -> Project:
        """
        Creates a new project document for a user.
        """
        project = Project(
            owner_id=owner_id, name=name, details=details, status="Active"
        )
        # Async Querying: Non-blocking operation
        await project.insert()
        return project

    async def get_project_by_id(
        self, project_id: PydanticObjectId, owner_id: PydanticObjectId
    ) -> Optional[Project]:
        """
        Retrieves a specific project, ensuring ownership check.
        """
        return await Project.find_one(
            Project.id == project_id, Project.owner_id == owner_id
        )

    async def get_projects_by_owner(
        self, owner_id: PydanticObjectId, limit: int = 100
    ) -> List[Project]:
        """
        Retrieves a list of projects owned by a specific user.
        Uses the compound index for fast retrieval.
        """
        return (
            await Project.find(Project.owner_id == owner_id)
            .sort(-Project.created_at)
            .limit(limit)
            .to_list()
        )

    async def update_project(
        self,
        project_id: PydanticObjectId,
        owner_id: PydanticObjectId,
        updates: Dict[str, Any],
    ) -> Optional[Project]:
        """
        Updates the details of an existing project.
        """
        project = await self.get_project_by_id(project_id, owner_id)
        if project:
            # Update fields dynamically and set the updated_at timestamp
            project.details.update(updates.pop("details", {}))
            project.updated_at = datetime.utcnow()

            # Use Beanie's set operation for efficiency
            await project.set(updates)

            # Refetch to ensure latest state is returned (optional, but good practice)
            return await self.get_project_by_id(project_id, owner_id)

        return None

    async def delete_project(
        self, project_id: PydanticObjectId, owner_id: PydanticObjectId
    ) -> bool:
        """
        Logically deletes a project.
        """
        # In a real app, you might set a status like 'archived' instead of deleting
        result = await Project.delete({"_id": project_id, "owner_id": owner_id})
        return result.deleted_count > 0


data_service = DataService()
