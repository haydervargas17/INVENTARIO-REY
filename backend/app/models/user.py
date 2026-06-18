from __future__ import annotations

from sqlalchemy import Boolean, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.enums import UserRole, enum_values
from backend.app.models.mixins import BaseModelMixin


class User(BaseModelMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(80), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", values_callable=enum_values),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_products = relationship(
        "Product",
        back_populates="created_by_user",
        foreign_keys="Product.created_by",
    )
    updated_products = relationship(
        "Product",
        back_populates="updated_by_user",
        foreign_keys="Product.updated_by",
    )
    inventory_movements = relationship("InventoryMovement", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    revoked_tokens = relationship("RevokedToken", back_populates="user")
