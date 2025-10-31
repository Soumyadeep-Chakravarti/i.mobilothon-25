# backend/app/src/api/v1/ml.py
from typing import List

from fastapi import APIRouter, status
from pydantic import BaseModel
from services.ml import ml_service
from services.task import task_service

router = APIRouter()


class PredictionInput(BaseModel):
    features: List[float]
    metadata: str = ""


@router.post("/predict", status_code=status.HTTP_200_OK)
async def predict_sync(input: PredictionInput):
    """
    Synchronous endpoint for low-latency AI prediction requests.
    """
    # **API Layer** handling request validation (via Pydantic)
    result = ml_service.get_prediction(input.model_dump())
    return {"status": "success", "data": result}


@router.post("/batch-job/{data_id}", status_code=status.HTTP_202_ACCEPTED)
async def trigger_batch_inference(data_id: str):
    """
    Asynchronous endpoint for long-running batch inference jobs.
    Returns HTTP 202 Accepted and a task ID.
    """
    # **Data Flow** step 4 & 5: Heavy task handed to Task Layer
    task_id = ml_service.trigger_batch_inference(data_id)
    return {
        "status": "accepted",
        "message": "Batch inference job started in the background.",
        "task_id": task_id,
        "check_status_url": f"/api/v1/tasks/status/{task_id}",
    }


@router.get("/tasks/status/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str):
    """
    Retrieves the current status of any background job.
    """
    # Placeholder for a task status check endpoint
    status_data = task_service.get_task_status(task_id)
    return status_data
