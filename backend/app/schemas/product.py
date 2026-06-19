from uuid import UUID

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    reference: str = Field(min_length=1, max_length=80)
    name: str = Field(min_length=1, max_length=150)
    brand: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    photo_url: str = Field(min_length=1)
    cloudinary_public_id: str | None = Field(default=None, max_length=255)
    current_purchase_price: int = Field(ge=0)
    current_sale_price: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    brand: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1)
    photo_url: str | None = Field(default=None, min_length=1)
    cloudinary_public_id: str | None = Field(default=None, max_length=255)
    current_purchase_price: int | None = Field(default=None, ge=0)
    current_sale_price: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: UUID
    reference: str
    name: str
    brand: str
    description: str
    photo_url: str
    cloudinary_public_id: str | None
    current_purchase_price: int
    current_sale_price: int
    is_active: bool


class ProductImageUploadResponse(BaseModel):
    product: ProductResponse
    secure_url: str
    optimized_url: str
    public_id: str
    width: int
    height: int
    format: str
    file_size: int
