from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    Gender: int = Field(..., ge=0, le=1, description="0 = Female, 1 = Male")
    AGE: int = Field(..., ge=1, le=120, description="Age in years (1-120)")
    Urea: float = Field(..., ge=0.5, le=200.0, description="Blood urea (mg/dL)")
    Cr: float = Field(..., ge=0.1, le=50.0, description="Creatinine (mg/dL)")
    HbA1c: float = Field(..., ge=2.0, le=20.0, description="Glycated hemoglobin (%)")
    Chol: float = Field(..., ge=1.0, le=20.0, description="Total cholesterol (mmol/L)")
    TG: float = Field(..., ge=0.1, le=30.0, description="Triglycerides (mmol/L)")
    HDL: float = Field(..., ge=0.1, le=10.0, description="HDL cholesterol (mmol/L)")
    LDL: float = Field(..., ge=0.1, le=15.0, description="LDL cholesterol (mmol/L)")
    VLDL: float = Field(..., ge=0.1, le=10.0, description="VLDL cholesterol (mmol/L)")
    BMI: float = Field(..., ge=10.0, le=80.0, description="Body Mass Index (kg/m²)")


CLASS_LABELS = {
    0: "No diabético",
    1: "Predicción de diabetes",
    2: "Diabético",
}


class PredictionResponse(BaseModel):
    predicted_class: int
    label: str
