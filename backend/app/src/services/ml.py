# backend/app/src/services/ml.py
from typing import Any, Dict

from core.config import settings


class MLService:
    """
    Handles AI model predictions and recommendation logic.
    """

    def __init__(self):
        # In a real app, model loading would occur here.
        # e.g., self.model = load_model("path/to/model")
        print("ML Service initialized: Model placeholder loaded.")

    def get_prediction(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes synchronous, low-latency AI inference.
        """
        # Simulate inference based on input features
        features = input_data.get("features", [])

        # Simple placeholder logic
        prediction_score = sum(features) / len(features) if features else 0

        return {
            "prediction": "high" if prediction_score > 0.5 else "low",
            "score": round(prediction_score, 4),
            "model_version": "v1.0",
        }

    def trigger_batch_inference(self, data_id: str) -> str:
        """
        Triggers a long-running, batch inference job using the Task Service.
        """
        # **ML Service** interacting asynchronously via internal routes (Task Layer)
        from services.task import task_service

        task_payload = {"data_source_id": data_id, "mode": "batch"}
        task_id = task_service.submit_report_generation(
            user_id="SYSTEM", payload=task_payload
        )
        return task_id


ml_service = MLService()
