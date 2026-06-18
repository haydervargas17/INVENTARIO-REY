from __future__ import annotations

from uuid import UUID

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import INET, JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.models.enums import AuditAction, enum_values
from backend.app.models.mixins import BaseModelMixin


class AuditLog(BaseModelMixin, Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[UUID | None] = mapped_column(
        PostgresUUID(as_uuid=True),
        ForeignKey("users.id"),
    )
    action: Mapped[AuditAction] = mapped_column(
        Enum(AuditAction, name="audit_action", values_callable=enum_values),
        nullable=False,
    )
    entity_name: Mapped[str | None] = mapped_column(String(80))
    entity_id: Mapped[UUID | None] = mapped_column(PostgresUUID(as_uuid=True))
    ip_address: Mapped[str | None] = mapped_column(INET)
    metadata_: Mapped[dict | None] = mapped_column("metadata", JSONB)

    user = relationship("User", back_populates="audit_logs")
