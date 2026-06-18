from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import RevokedToken


class TokenRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def is_revoked(self, token_jti: str) -> bool:
        revoked_token = self.db.scalar(
            select(RevokedToken).where(
                RevokedToken.token_jti == token_jti,
                RevokedToken.deleted_at.is_(None),
            )
        )
        return revoked_token is not None

    def revoke(
        self,
        *,
        token_jti: str,
        user_id,
        expires_at: datetime,
        reason: str = "logout",
    ) -> RevokedToken:
        revoked_token = RevokedToken(
            token_jti=token_jti,
            user_id=user_id,
            expires_at=expires_at,
            reason=reason,
        )
        self.db.add(revoked_token)
        return revoked_token
