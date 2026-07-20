"""
Prediction endpoints.

Replaces the Streamlit "widgets -> instant recompute" flow with explicit
POST endpoints. The frontend (or any client: curl, mobile app, another
service) sends JSON, gets JSON back.
"""
from fastapi import APIRouter, HTTPException

from app.models.schemas import DiabetesInputV1, DiabetesInputV2, PredictionResponse
from app.services.prediction import predictor_v1, predictor_v2, ModelNotLoadedError

router = APIRouter(prefix="/api/predict", tags=["prediction"])


@router.post("/v1", response_model=PredictionResponse)
def predict_v1(payload: DiabetesInputV1) -> PredictionResponse:
    """Predict diabetes risk using the clean production model (model6)."""
    try:
        return predictor_v1.predict(payload)
    except ModelNotLoadedError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/v2", response_model=PredictionResponse)
def predict_v2(payload: DiabetesInputV2) -> PredictionResponse:
    """Predict diabetes risk using the backend-aligned pipeline model."""
    try:
        return predictor_v2.predict(payload)
    except ModelNotLoadedError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/status")
def model_status() -> dict:
    """Quick health check for whether model artifacts loaded correctly."""
    return {
        "v1_ready": predictor_v1.is_ready,
        "v2_ready": predictor_v2.is_ready,
    }
