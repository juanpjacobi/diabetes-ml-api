from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.prediction import router as prediction_router

app = FastAPI(title="Diabetes Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "https://diabetes-ml-client.netlify.app",
    ],
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

app.include_router(prediction_router)


@app.get("/health")
def health():
    return {"status": "ok"}
