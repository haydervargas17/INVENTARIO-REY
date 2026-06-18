from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models import AuditAction, InventoryItem, InventoryMovement, MovementType
from backend.app.repositories.audit_repository import AuditRepository
from backend.app.repositories.color_repository import ColorRepository
from backend.app.repositories.inventory_repository import InventoryRepository
from backend.app.repositories.product_repository import ProductRepository
from backend.app.schemas.inventory import InventoryEntryRequest
from backend.app.utils.colors import build_color_signature


class InventoryValidationError(Exception):
    """Raised when inventory business rules are violated."""


class InventoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.colors = ColorRepository(db)
        self.products = ProductRepository(db)
        self.inventory = InventoryRepository(db)
        self.audit_logs = AuditRepository(db)

    def list_inventory(
        self,
        *,
        search: str | None = None,
        size: float | None = None,
        location_type=None,
        available_only: bool = False,
        low_stock_only: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> list[InventoryItem]:
        return self.inventory.list(
            search=search,
            size=size,
            location_type=location_type,
            available_only=available_only,
            low_stock_only=low_stock_only,
            limit=limit,
            offset=offset,
        )

    def register_entry(self, payload: InventoryEntryRequest, user_id: UUID) -> tuple[InventoryItem, InventoryMovement]:
        colors = self.colors.get_active_by_ids(payload.color_ids)
        if len(colors) != len(set(payload.color_ids)):
            raise InventoryValidationError("One or more colors are invalid.")

        sorted_colors = sorted(colors, key=lambda color: color.normalized_name)
        sorted_color_ids = [color.id for color in sorted_colors]
        color_signature = build_color_signature(sorted_colors)

        product = self.products.get_by_reference(payload.product.reference)
        if product is None:
            product = self.products.create(payload.product, user_id=user_id)
            self.db.flush()
            self.audit_logs.create(
                action=AuditAction.CREATE,
                user_id=user_id,
                entity_name="products",
                entity_id=product.id,
                metadata={"reference": product.reference},
            )
        else:
            self.products.update_prices(
                product,
                purchase_price=payload.purchase_unit_price,
                sale_price=payload.sale_unit_price,
                user_id=user_id,
            )

        existing_item = self.inventory.find_existing(
            product_id=product.id,
            size=payload.size,
            color_signature=color_signature,
            location_type=payload.location_type,
            location_detail=payload.location_detail,
        )

        if existing_item is None:
            previous_quantity = 0
            new_quantity = payload.quantity
            item = self.inventory.create_item(
                product_id=product.id,
                size=payload.size,
                color_signature=color_signature,
                location_type=payload.location_type,
                location_detail=payload.location_detail,
                quantity=payload.quantity,
                color_ids=sorted_color_ids,
                user_id=user_id,
            )
        else:
            previous_quantity = existing_item.quantity
            existing_item.quantity += payload.quantity
            existing_item.updated_by = user_id
            new_quantity = existing_item.quantity
            item = existing_item

        movement = self.inventory.create_movement(
            inventory_item_id=item.id,
            movement_type=MovementType.IN,
            quantity_delta=payload.quantity,
            previous_quantity=previous_quantity,
            new_quantity=new_quantity,
            purchase_unit_price=payload.purchase_unit_price,
            sale_unit_price=payload.sale_unit_price,
            reason=payload.reason,
            user_id=user_id,
        )
        self.audit_logs.create(
            action=AuditAction.INVENTORY_IN,
            user_id=user_id,
            entity_name="inventory_items",
            entity_id=item.id,
            metadata={
                "reference": product.reference,
                "quantity_delta": payload.quantity,
                "previous_quantity": previous_quantity,
                "new_quantity": new_quantity,
            },
        )
        self.db.commit()
        self.db.refresh(item)
        self.db.refresh(movement)
        return item, movement
