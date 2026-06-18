from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import Color


class ColorRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_active(self) -> list[Color]:
        return list(
            self.db.scalars(
                select(Color)
                .where(Color.deleted_at.is_(None), Color.is_active.is_(True))
                .order_by(Color.name)
            )
        )

    def get_active_by_ids(self, color_ids: list[UUID]) -> list[Color]:
        return list(
            self.db.scalars(
                select(Color).where(
                    Color.id.in_(color_ids),
                    Color.deleted_at.is_(None),
                    Color.is_active.is_(True),
                )
            )
        )
