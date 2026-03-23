from fastapi import APIRouter

from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.model_service import predict

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict_diabetes(request: PredictionRequest) -> PredictionResponse:
    return predict(request)
