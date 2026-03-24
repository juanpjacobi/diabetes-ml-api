import json
import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.prediction import router as prediction_router
from app.core.config import METADATA_PATH

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Diabetes Prediction API")


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    logger.info(
        "%s %s",
        request.method,
        request.url.path,
        extra={
            "request_id": request_id,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    response.headers["X-Request-ID"] = request_id
    return response

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
    response = {"status": "ok"}
    if METADATA_PATH.exists():
        metadata = json.loads(METADATA_PATH.read_text())
        response["model_version"] = metadata.get("model_version")
        response["accuracy"] = metadata.get("accuracy")
        response["trained_at"] = metadata.get("trained_at")
        response["features"] = metadata.get("features")
    return response
