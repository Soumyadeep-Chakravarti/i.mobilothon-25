# backend/app/src/api/v1/notification.py (NEW FILE)
from fastapi import APIRouter, status
from pydantic import BaseModel, Field
from services.notification import notification_service

router = APIRouter()


class NotificationRequest(BaseModel):
    user_id: str = Field(..., description="Target MongoDB user ID.")
    message: str = Field(..., max_length=500)
    type: str = Field("email", description="Type of notification: email, push, in-app.")


@router.post("/send", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(request: NotificationRequest):
    """
    Triggers an asynchronous notification dispatch.
    Returns HTTP 202 Accepted (Data Flow Step 5).
    """
    task_id = notification_service.send_user_alert(
        user_id=request.user_id, message=request.message, type=request.type
    )

    return {
        "status": "accepted",
        "message": f"Notification task accepted. Task will execute shortly.",
        "task_id": task_id,
    }
