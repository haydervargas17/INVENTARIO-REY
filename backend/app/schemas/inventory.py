from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from backend.app.models.enums import LocationType
from backend.app.schemas.catalog import ColorResponse
from backend.app.schemas.product import ProductCreate, ProductResponse


class InventoryEntryRequest(BaseModel):
    product: ProductCreate
    size: float = Field(gt=0)
    color_ids: list[UUID] = Field(min_length=1)
    location_type: LocationType
    location_detail: str = Field(min_length=1, max_length=150)
    quantity: int = Field(gt=0)
    purchase_unit_price: int = Field(ge=0)
    sale_unit_price: int = Field(ge=0)
    reason: str = Field(default="Ingreso de mercancia", min_length=1)

    @model_validator(mode="after")
    def ensure_unique_colors(self) -> "InventoryEntryRequest":
        if len(set(self.color_ids)) != len(self.color_ids):
            raise ValueError("Los colores seleccionados no deben repetirse.")
        return self


class InventoryMovementResponse(BaseModel):
    id: UUID
    movement_type: str
    quantity_delta: int
    previous_quantity: int
    new_quantity: int
    purchase_unit_price: int | None
    sale_unit_price: int | None
    reason: str


class InventoryItemResponse(BaseModel):
    id: UUID
    product: ProductResponse
    size: float
    color_signature: str
    colors: list[ColorResponse]
    location_type: LocationType
    location_detail: str
    quantity: int
    low_stock_threshold: int
    is_low_stock: bool


class InventoryEntryResponse(BaseModel):
    inventory_item: InventoryItemResponse
    movement: InventoryMovementResponse
