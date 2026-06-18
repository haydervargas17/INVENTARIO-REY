from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.mixins import BaseModelMixin


class Color(BaseModelMixin, Base):
    __tablename__ = "colors"

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    inventory_item_colors = relationship("InventoryItemColor", back_populates="color")
