from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models import AuditAction, AuditLog


class AuditRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        *,
        action: AuditAction,
        user_id: UUID | None = None,
        entity_name: str | None = None,
        entity_id: UUID | None = None,
        ip_address: str | None = None,
        metadata: dict | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            ip_address=ip_address,
            metadata_=metadata,
        )
        self.db.add(audit_log)
        return audit_log
