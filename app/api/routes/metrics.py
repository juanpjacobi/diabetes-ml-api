from fastapi import APIRouter

from app.db.database import get_metrics
from app.schemas.prediction import CLASS_LABELS

router = APIRouter()


@router.get("/metrics")
def metrics():
    data = get_metrics()

    by_class_labeled = {
        cls: {"label": CLASS_LABELS[int(cls)], "count": count}
        for cls, count in data["by_class"].items()
    }

    return {
        "total_predictions": data["total_predictions"],
        "by_class": by_class_labeled,
        "avg_duration_ms": data["avg_duration_ms"],
    }