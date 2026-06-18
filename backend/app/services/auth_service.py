from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.config import get_settings
from backend.app.models import AuditAction, User
from backend.app.repositories.audit_repository import AuditRepository
from backend.app.repositories.token_repository import TokenRepository
from backend.app.repositories.user_repository import UserRepository
from backend.app.security.jwt import create_access_token
from backend.app.security.password import verify_password


class AuthError(Exception):
    """Raised when authentication fails."""


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.users = UserRepository(db)
        self.tokens = TokenRepository(db)
        self.audit_logs = AuditRepository(db)

    def authenticate(self, username: str, password: str, ip_address: str | None = None) -> tuple[User, str]:
        user = self.users.get_by_username(username)

        if user is None or not user.is_active or not verify_password(password, user.password_hash):
            raise AuthError("Invalid username or password.")

        token, token_jti, expires_at = create_access_token(str(user.id))
        self.audit_logs.create(
            action=AuditAction.LOGIN,
            user_id=user.id,
            entity_name="users",
            entity_id=user.id,
            ip_address=ip_address,
            metadata={"token_jti": token_jti, "expires_at": expires_at.isoformat()},
        )
        self.db.commit()
        return user, token

    def logout(
        self,
        *,
        user_id: UUID,
        token_jti: str,
        expires_at: datetime,
        ip_address: str | None = None,
    ) -> None:
        if not self.tokens.is_revoked(token_jti):
            self.tokens.revoke(token_jti=token_jti, user_id=user_id, expires_at=expires_at)

        self.audit_logs.create(
            action=AuditAction.LOGOUT,
            user_id=user_id,
            entity_name="users",
            entity_id=user_id,
            ip_address=ip_address,
            metadata={"token_jti": token_jti},
        )
        self.db.commit()

    @staticmethod
    def token_expire_hours() -> int:
        return get_settings().access_token_expire_hours
