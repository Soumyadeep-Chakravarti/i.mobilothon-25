# backend/app/src/tasks/worker.py
from time import sleep

from celery import Celery
from core.config import settings

# Initialize Celery using Redis as the broker
celery_app = Celery(
    "v13_tasks",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["services.task"],  # Include task definitions from the service layer
)

# Optional: Configure Celery for better resilience
celery_app.conf.update(
    task_track_started=True,
    task_send_sent_event=True,
    task_default_retry_limit=settings.TASK_MAX_RETRIES,
    task_default_retry_delay=60,  # seconds
)


@celery_app.task(bind=True)
def example_long_running_task(self, data: dict):
    """
    Placeholder for a heavy, background job (e.g., report generation).
    """
    try:
        print(f"Starting heavy task for data: {data}")
        # Simulate long-running I/O or computation
        sleep(5)
        print("Task completed successfully.")
        return {"status": "completed", "result": f"Processed {len(data)} items."}
    except Exception as e:
        # **Resilience** principle: structured retry
        raise self.retry(exc=e, countdown=2)
