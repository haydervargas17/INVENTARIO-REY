from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.api.v1.mappers import map_inventory_item, map_inventory_movement
from backend.app.database import get_db
from backend.app.models import LocationType, User
from backend.app.schemas.inventory import (
    InventoryAdjustmentRequest,
    InventoryEntryRequest,
    InventoryExitRequest,
)
from backend.app.services.inventory_service import (
    InventoryItemNotFoundError,
    InventoryService,
    InventoryValidationError,
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("")
def list_inventory(
    search: str | None = None,
    size: float | None = Query(default=None, gt=0),
    location_type: LocationType | None = None,
    available_only: bool = False,
    low_stock_only: bool = False,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    items = InventoryService(db).list_inventory(
        search=search,
        size=size,
        location_type=location_type,
        available_only=available_only,
        low_stock_only=low_stock_only,
        limit=limit,
        offset=offset,
    )

    return {
        "success": True,
        "message": "Listado de inventario.",
        "data": [map_inventory_item(item).model_dump(mode="json") for item in items],
        "errors": None,
    }


@router.post("/entries", status_code=status.HTTP_201_CREATED)
def register_inventory_entry(
    payload: InventoryEntryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        item, movement = InventoryService(db).register_entry(payload, user_id=current_user.id)
    except InventoryValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Entrada de inventario registrada.",
        "data": {
            "inventory_item": map_inventory_item(item).model_dump(mode="json"),
            "movement": map_inventory_movement(movement).model_dump(mode="json"),
        },
        "errors": None,
    }


@router.post("/{inventory_item_id}/exits", status_code=status.HTTP_201_CREATED)
def register_inventory_exit(
    inventory_item_id: UUID,
    payload: InventoryExitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        item, movement = InventoryService(db).register_exit(
            inventory_item_id=inventory_item_id,
            payload=payload,
            user_id=current_user.id,
        )
    except InventoryItemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Existencia no encontrada.") from exc
    except InventoryValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Salida de inventario registrada.",
        "data": {
            "inventory_item": map_inventory_item(item).model_dump(mode="json"),
            "movement": map_inventory_movement(movement).model_dump(mode="json"),
        },
        "errors": None,
    }


@router.post("/{inventory_item_id}/adjustments", status_code=status.HTTP_201_CREATED)
def register_inventory_adjustment(
    inventory_item_id: UUID,
    payload: InventoryAdjustmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        item, movement = InventoryService(db).register_adjustment(
            inventory_item_id=inventory_item_id,
            payload=payload,
            user_id=current_user.id,
        )
    except InventoryItemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Existencia no encontrada.") from exc
    except InventoryValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Ajuste de inventario registrado.",
        "data": {
            "inventory_item": map_inventory_item(item).model_dump(mode="json"),
            "movement": map_inventory_movement(movement).model_dump(mode="json"),
        },
        "errors": None,
    }


@router.get("/{inventory_item_id}/movements")
def list_inventory_movements(
    inventory_item_id: UUID,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    _current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    try:
        movements = InventoryService(db).list_movements(
            inventory_item_id=inventory_item_id,
            limit=limit,
            offset=offset,
        )
    except InventoryItemNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Existencia no encontrada.") from exc

    return {
        "success": True,
        "message": "Historial de movimientos.",
        "data": [map_inventory_movement(movement).model_dump(mode="json") for movement in movements],
        "errors": None,
    }
