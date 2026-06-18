from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select, and_, func, select
from sqlalchemy.orm import Session, joinedload

from backend.app.models import (
    InventoryItem,
    InventoryItemColor,
    InventoryMovement,
    LocationType,
    MovementType,
    Product,
)


class InventoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def base_query(self) -> Select:
        return (
            select(InventoryItem)
            .options(
                joinedload(InventoryItem.product),
                joinedload(InventoryItem.colors).joinedload(InventoryItemColor.color),
            )
            .where(InventoryItem.deleted_at.is_(None))
        )

    def get_by_id(self, inventory_item_id: UUID) -> InventoryItem | None:
        return self.db.scalars(
            self.base_query().where(InventoryItem.id == inventory_item_id)
        ).unique().first()

    def find_existing(
        self,
        *,
        product_id: UUID,
        size: float,
        color_signature: str,
        location_type: LocationType,
        location_detail: str,
    ) -> InventoryItem | None:
        return self.db.scalars(
            self.base_query().where(
                InventoryItem.product_id == product_id,
                InventoryItem.size == size,
                InventoryItem.color_signature == color_signature,
                InventoryItem.location_type == location_type,
                func.lower(InventoryItem.location_detail) == location_detail.lower(),
            )
        ).unique().first()

    def list(
        self,
        *,
        search: str | None = None,
        size: float | None = None,
        location_type: LocationType | None = None,
        available_only: bool = False,
        low_stock_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[InventoryItem]:
        stmt = self.base_query().join(Product).order_by(Product.reference, InventoryItem.size)

        filters = []
        if search:
            pattern = f"%{search}%"
            filters.append(
                Product.reference.ilike(pattern)
                | Product.name.ilike(pattern)
                | Product.description.ilike(pattern)
                | Product.brand.ilike(pattern)
            )
        if size is not None:
            filters.append(InventoryItem.size == size)
        if location_type is not None:
            filters.append(InventoryItem.location_type == location_type)
        if available_only:
            filters.append(InventoryItem.quantity > 0)
        if low_stock_only:
            filters.append(InventoryItem.quantity <= InventoryItem.low_stock_threshold)

        if filters:
            stmt = stmt.where(and_(*filters))

        return list(self.db.scalars(stmt.limit(limit).offset(offset)).unique())

    def create_item(
        self,
        *,
        product_id: UUID,
        size: float,
        color_signature: str,
        location_type: LocationType,
        location_detail: str,
        quantity: int,
        color_ids: list[UUID],
        user_id: UUID,
    ) -> InventoryItem:
        item = InventoryItem(
            product_id=product_id,
            size=size,
            color_signature=color_signature,
            location_type=location_type,
            location_detail=location_detail.strip(),
            quantity=quantity,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(item)
        self.db.flush()

        for sort_order, color_id in enumerate(color_ids):
            self.db.add(
                InventoryItemColor(
                    inventory_item_id=item.id,
                    color_id=color_id,
                    sort_order=sort_order,
                )
            )

        return item

    def create_movement(
        self,
        *,
        inventory_item_id: UUID,
        movement_type: MovementType,
        quantity_delta: int,
        previous_quantity: int,
        new_quantity: int,
        purchase_unit_price: int | None,
        sale_unit_price: int | None,
        reason: str,
        user_id: UUID,
    ) -> InventoryMovement:
        movement = InventoryMovement(
            inventory_item_id=inventory_item_id,
            movement_type=movement_type,
            quantity_delta=quantity_delta,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            purchase_unit_price=purchase_unit_price,
            sale_unit_price=sale_unit_price,
            reason=reason,
            user_id=user_id,
        )
        self.db.add(movement)
        return movement
