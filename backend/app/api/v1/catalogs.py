from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.api.v1.mappers import map_color
from backend.app.database import get_db
from backend.app.models import User
from backend.app.repositories.color_repository import ColorRepository

router = APIRouter(prefix="/catalogs", tags=["catalogs"])


@router.get("/colors")
def list_colors(
    _current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    colors = ColorRepository(db).list_active()

    return {
        "success": True,
        "message": "Catalogo de colores.",
        "data": [map_color(color).model_dump(mode="json") for color in colors],
        "errors": None,
    }
