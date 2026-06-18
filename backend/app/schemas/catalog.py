from uuid import UUID

from pydantic import BaseModel


class ColorResponse(BaseModel):
    id: UUID
    name: str
    normalized_name: str
    is_active: bool
