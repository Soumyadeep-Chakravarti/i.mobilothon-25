# backend/app/src/services/task.py (UPDATED)
from typing import Any, Dict

from services.notification import notification_service
from tasks.worker import celery_app


# --- New Celery Task Definition for Notifications ---
# This function is executed by the Celery worker in the background.
@celery_app.task(bind=True, max_retries=3)
def dispatch_notification(self, payload: Dict[str, Any]):
    """
    Celery task that calls the synchronous execution logic in the Notification Service.
    Implements Task Resilience (retry policy).
    """
    try:
        notification_service._execute_dispatch(payload)
    except Exception as e:
        # **Resilience**: Structured fallback/retry system
        raise self.retry(exc=e, countdown=10)


# ----------------------------------------------------


class TaskService:
    """
    Encapsulates logic for submitting and monitoring background tasks. (Existing class)
    """

    # ... (submit_report_generation and get_task_status methods remain the same) ...

    @staticmethod
    def submit_notification_dispatch(payload: Dict[str, Any]) -> str:
        """
        Submits a notification request to the task queue.
        """
        task = dispatch_notification.delay(payload)
        return task.id


task_service = TaskService()
