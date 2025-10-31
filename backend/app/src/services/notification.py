# backend/app/src/services/notification.py
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# NOTE: We intentionally import the task_service here, but the actual
# implementation of the Celery task itself will be put in services/task.py
# for organizational clarity (keeping Celery task definitions separate from service logic).


class NotificationService:
    """
    Handles logic for sending push/email/in-app alerts.
    Uses Task Layer for background dispatch.
    """

    def send_user_alert(self, user_id: str, message: str, type: str = "in-app") -> str:
        """
        Public method to trigger a background notification.
        """
        # Lazy import to avoid circular dependency issues at the module level
        from services.task import task_service

        payload = {
            "user_id": user_id,
            "message": message,
            "type": type,
        }

        # Dispatch the job to the Task Service
        logger.info(f"Dispatching background notification for user {user_id}...")
        task_id = task_service.submit_notification_dispatch(payload)

        return task_id

    # The actual synchronous dispatch function (used by the Celery worker)
    def _execute_dispatch(self, payload: Dict[str, Any]):
        """
        Synchronous, blocking function run ONLY by the Celery worker.
        Simulates interaction with an external provider (e.g., SendGrid, Firebase).
        """
        user_id = payload.get("user_id", "Unknown")
        message = payload.get("message", "No message")
        type = payload.get("type", "in-app")

        logger.info(
            f"[Worker] Successfully dispatched {type} alert to {user_id}: '{message[:20]}...'"
        )
        # --- Actual API call to a provider would go here ---
        # time.sleep(1) # Simulate network latency
        # ---------------------------------------------------


notification_service = NotificationService()
