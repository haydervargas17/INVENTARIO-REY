from fastapi import APIRouter

from backend.app.config import get_settings
from backend.app.database import ping_database

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, object]:
    settings = get_settings()
    return {
        "success": True,
        "message": "API is running.",
        "data": {
            "app": settings.app_name,
            "environment": settings.app_env,
        },
        "errors": None,
    }


@router.get("/health/database")
def database_health_check() -> dict[str, object]:
    ping_database()
    return {
        "success": True,
        "message": "Database connection is healthy.",
        "data": {"database": "ok"},
        "errors": None,
    }
