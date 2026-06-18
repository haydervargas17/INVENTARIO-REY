from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.mixins import BaseModelMixin


class Product(BaseModelMixin, Base):
    __tablename__ = "products"

    reference: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(Text, nullable=False)
    cloudinary_public_id: Mapped[str | None] = mapped_column(String(255))
    current_purchase_price: Mapped[int] = mapped_column(Integer, nullable=False)
    current_sale_price: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_by: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
    )
    updated_by: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
    )

    created_by_user = relationship(
        "User",
        back_populates="created_products",
        foreign_keys=[created_by],
    )
    updated_by_user = relationship(
        "User",
        back_populates="updated_products",
        foreign_keys=[updated_by],
    )
    inventory_items = relationship("InventoryItem", back_populates="product")
