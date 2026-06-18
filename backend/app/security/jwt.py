from datetime import UTC, datetime, timedelta
from uuid import uuid4

from jose import JWTError, jwt

from backend.app.config import get_settings


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> tuple[str, str, datetime]:
    settings = get_settings()
    expires_at = datetime.now(UTC) + (
        expires_delta or timedelta(hours=settings.access_token_expire_hours)
    )
    token_jti = str(uuid4())
    payload = {
        "sub": subject,
        "jti": token_jti,
        "exp": expires_at,
        "iat": datetime.now(UTC),
        "type": "access",
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, token_jti, expires_at


def decode_access_token(token: str) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise ValueError("Invalid token.") from exc

    if payload.get("type") != "access":
        raise ValueError("Invalid token type.")

    return payload
