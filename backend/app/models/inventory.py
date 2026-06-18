from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.enums import LocationType, MovementType, enum_values
from backend.app.models.mixins import BaseModelMixin


class InventoryItem(BaseModelMixin, Base):
    __tablename__ = "inventory_items"

    product_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("products.id"),
        nullable=False,
    )
    size: Mapped[float] = mapped_column(Numeric(4, 1), nullable=False)
    color_signature: Mapped[str] = mapped_column(String(255), nullable=False)
    location_type: Mapped[LocationType] = mapped_column(
        Enum(LocationType, name="location_type", values_callable=enum_values),
        nullable=False,
    )
    location_detail: Mapped[str] = mapped_column(String(150), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
    )
    updated_by: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
    )

    product = relationship("Product", back_populates="inventory_items")
    colors = relationship("InventoryItemColor", back_populates="inventory_item")
    movements = relationship("InventoryMovement", back_populates="inventory_item")


class InventoryItemColor(BaseModelMixin, Base):
    __tablename__ = "inventory_item_colors"

    inventory_item_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_items.id"),
        nullable=False,
    )
    color_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("colors.id"),
        nullable=False,
    )
    sort_order: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)

    inventory_item = relationship("InventoryItem", back_populates="colors")
    color = relationship("Color", back_populates="inventory_item_colors")


class InventoryMovement(BaseModelMixin, Base):
    __tablename__ = "inventory_movements"

    inventory_item_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("inventory_items.id"),
        nullable=False,
    )
    movement_type: Mapped[MovementType] = mapped_column(
        Enum(MovementType, name="movement_type", values_callable=enum_values),
        nullable=False,
    )
    quantity_delta: Mapped[int] = mapped_column(Integer, nullable=False)
    previous_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    new_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    purchase_unit_price: Mapped[int | None] = mapped_column(Integer)
    sale_unit_price: Mapped[int | None] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    inventory_item = relationship("InventoryItem", back_populates="movements")
    user = relationship("User", back_populates="inventory_movements")
