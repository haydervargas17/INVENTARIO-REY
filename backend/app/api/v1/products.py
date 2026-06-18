from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.api.v1.mappers import map_product
from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas.product import ProductCreate, ProductUpdate
from backend.app.services.product_service import (
    ProductConflictError,
    ProductNotFoundError,
    ProductService,
)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def list_products(
    search: str | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    products = ProductService(db).list_products(search=search, limit=limit, offset=offset)

    return {
        "success": True,
        "message": "Listado de referencias.",
        "data": [map_product(product).model_dump(mode="json") for product in products],
        "errors": None,
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        product = ProductService(db).create_product(payload, user_id=current_user.id)
    except ProductConflictError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una referencia con ese codigo.",
        ) from exc

    return {
        "success": True,
        "message": "Referencia creada.",
        "data": map_product(product).model_dump(mode="json"),
        "errors": None,
    }


@router.patch("/{product_id}")
def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        product = ProductService(db).update_product(
            product_id=product_id,
            payload=payload,
            user_id=current_user.id,
        )
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Referencia no encontrada.") from exc

    return {
        "success": True,
        "message": "Referencia actualizada.",
        "data": map_product(product).model_dump(mode="json"),
        "errors": None,
    }
