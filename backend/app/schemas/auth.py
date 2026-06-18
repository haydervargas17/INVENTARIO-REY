from uuid import UUID

from pydantic import BaseModel, Field

from backend.app.models.enums import UserRole


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1)


class AuthUserResponse(BaseModel):
    id: UUID
    username: str
    full_name: str
    role: UserRole


class LoginResponseData(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_hours: int
    user: AuthUserResponse


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: object | None = None
    errors: list[dict] | None = None
