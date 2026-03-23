from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    Gender: int = Field(..., ge=0, le=1, description="0 = Female, 1 = Male")
    AGE: int = Field(..., gt=0)
    Urea: float
    Cr: float
    HbA1c: float
    Chol: float
    TG: float
    HDL: float
    LDL: float
    VLDL: float
    BMI: float


CLASS_LABELS = {
    0: "No diabético",
    1: "Predicción de diabetes",
    2: "Diabético",
}


class PredictionResponse(BaseModel):
    predicted_class: int
    label: str
