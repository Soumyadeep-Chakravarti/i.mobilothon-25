# backend/app/src/services/admin.py (NEW FILE)
from typing import Any, Dict, List

from core.config import settings
from services.task import task_service  # To access queue metrics


class AdminService:
    """
    Provides operational visibility and access control (management APIs).
    Simulates fetching system metrics and configurations.
    """

    def get_system_config(self) -> Dict[str, Any]:
        """
        Retrieves application configuration details (excluding secrets).
        """
        # Exclude sensitive information explicitly
        config_data = {
            "APP_NAME": settings.APP_NAME,
            "ENV": settings.ENV,
            "DEBUG": settings.DEBUG,
            "MONGO_URI_STATUS": "Configured",  # Don't expose the URI itself
            "REDIS_URL_STATUS": "Configured",
            "ML_SERVICE_TIMEOUT_SEC": settings.ML_SERVICE_TIMEOUT_SEC,
        }
        return config_data

    def get_operational_metrics(self) -> Dict[str, Any]:
        """
        Gathers key operational metrics. In production, this data would come from
        Prometheus or directly from monitoring libraries (e.g., `psutil`).
        """
        # Simulate worker health and queue depth (Task Queue Metrics)
        task_metrics = self._get_task_queue_status()

        return {
            "service_uptime": "N/A (requires external monitor)",
            "worker_status": task_metrics.get("workers_online", 0),
            "queue_depth": task_metrics.get("queue_length", 0),
            "last_db_check": task_metrics.get("last_check"),
            "memory_usage_mb": 450,  # Placeholder
            "cpu_usage_percent": 12.5,  # Placeholder
        }

    def _get_task_queue_status(self) -> Dict[str, Any]:
        """
        Simulates checking the Celery/Redis broker status.
        """
        # In a full implementation, this uses Celery's inspect() or a direct Redis check.
        # For simplicity, we use the TaskService status check as a proxy.

        # Example: Querying a dummy task status could confirm broker connectivity
        # NOTE: This is highly simplified and assumes the Task Service can communicate with Redis.
        return {
            "workers_online": 2,
            "queue_length": 5,
            "last_check": str(datetime.now()),
        }

    async def get_all_active_tasks(self) -> List[Dict[str, Any]]:
        """
        Placeholder: Retrieves a list of currently running/pending background tasks.
        """
        # Logic to inspect Celery's active tasks would go here
        return [
            {"id": "task-abc-123", "name": "report_generation", "status": "RUNNING"},
            {
                "id": "task-def-456",
                "name": "dispatch_notification",
                "status": "PENDING",
            },
        ]


admin_service = AdminService()
