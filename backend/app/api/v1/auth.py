from datetime import datetime
from ipaddress import ip_address

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_token_context, get_current_user
from backend.app.database import get_db
from backend.app.models import User
from backend.app.schemas.auth import AuthUserResponse, LoginRequest, LoginResponseData
from backend.app.services.auth_service import AuthError, AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def _client_ip(request: Request) -> str | None:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        candidate = forwarded_for.split(",", 1)[0].strip()
    else:
        candidate = request.client.host if request.client else None

    if candidate is None:
        return None

    try:
        ip_address(candidate)
    except ValueError:
        return None

    return candidate


def _user_response(user: User) -> AuthUserResponse:
    return AuthUserResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
    )


@router.post("/login")
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    auth_service = AuthService(db)

    try:
        user, access_token = auth_service.authenticate(
            username=payload.username,
            password=payload.password,
            ip_address=_client_ip(request),
        )
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        ) from exc

    data = LoginResponseData(
        access_token=access_token,
        expires_in_hours=auth_service.token_expire_hours(),
        user=_user_response(user),
    )

    return {
        "success": True,
        "message": "Inicio de sesion exitoso.",
        "data": data.model_dump(mode="json"),
        "errors": None,
    }


@router.post("/logout")
def logout(
    request: Request,
    current_user: User = Depends(get_current_user),
    token_context: tuple[str, datetime] = Depends(get_current_token_context),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    token_jti, expires_at = token_context
    AuthService(db).logout(
        user_id=current_user.id,
        token_jti=token_jti,
        expires_at=expires_at,
        ip_address=_client_ip(request),
    )

    return {
        "success": True,
        "message": "Cierre de sesion exitoso.",
        "data": None,
        "errors": None,
    }


@router.get("/me")
def me(current_user: User = Depends(get_current_user)) -> dict[str, object]:
    return {
        "success": True,
        "message": "Usuario autenticado.",
        "data": _user_response(current_user).model_dump(mode="json"),
        "errors": None,
    }
