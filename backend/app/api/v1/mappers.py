from backend.app.models import Color, InventoryItem, InventoryItemColor, InventoryMovement, Product
from backend.app.schemas.catalog import ColorResponse
from backend.app.schemas.inventory import (
    InventoryItemResponse,
    InventoryMovementResponse,
)
from backend.app.schemas.product import ProductResponse


def map_color(color: Color) -> ColorResponse:
    return ColorResponse(
        id=color.id,
        name=color.name,
        normalized_name=color.normalized_name,
        is_active=color.is_active,
    )


def map_product(product: Product) -> ProductResponse:
    return ProductResponse(
        id=product.id,
        reference=product.reference,
        name=product.name,
        brand=product.brand,
        description=product.description,
        photo_url=product.photo_url,
        cloudinary_public_id=product.cloudinary_public_id,
        current_purchase_price=product.current_purchase_price,
        current_sale_price=product.current_sale_price,
        is_active=product.is_active,
    )


def map_inventory_item(item: InventoryItem) -> InventoryItemResponse:
    colors = sorted(
        (item_color for item_color in item.colors if item_color.deleted_at is None),
        key=lambda item_color: item_color.sort_order,
    )
    return InventoryItemResponse(
        id=item.id,
        product=map_product(item.product),
        size=float(item.size),
        color_signature=item.color_signature,
        colors=[map_color(item_color.color) for item_color in colors],
        location_type=item.location_type,
        location_detail=item.location_detail,
        quantity=item.quantity,
        low_stock_threshold=item.low_stock_threshold,
        is_low_stock=item.quantity <= item.low_stock_threshold,
    )


def map_inventory_movement(movement: InventoryMovement) -> InventoryMovementResponse:
    return InventoryMovementResponse(
        id=movement.id,
        movement_type=movement.movement_type.value,
        quantity_delta=movement.quantity_delta,
        previous_quantity=movement.previous_quantity,
        new_quantity=movement.new_quantity,
        purchase_unit_price=movement.purchase_unit_price,
        sale_unit_price=movement.sale_unit_price,
        reason=movement.reason,
    )
