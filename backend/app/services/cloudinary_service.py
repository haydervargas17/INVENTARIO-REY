from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from backend.app.config import get_settings

ALLOWED_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_SIZE_BYTES = 4 * 1024 * 1024


class ImageUploadError(Exception):
    """Raised when a product image cannot be uploaded."""


@dataclass(frozen=True)
class UploadedImage:
    secure_url: str
    optimized_url: str
    public_id: str
    width: int
    height: int
    format: str
    file_size: int


def _safe_public_reference(reference: str) -> str:
    normalized = reference.strip().lower()
    safe_chars = []
    for char in normalized:
        if char.isalnum() or char in {"-", "_"}:
            safe_chars.append(char)
        else:
            safe_chars.append("-")

    safe_reference = "".join(safe_chars).strip("-")
    return safe_reference or "product"


class CloudinaryImageService:
    def __init__(self) -> None:
        settings = get_settings()
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )

    def upload_product_image(
        self,
        *,
        reference: str,
        file: BinaryIO,
        content_type: str | None,
    ) -> UploadedImage:
        if content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
            raise ImageUploadError("Solo se permiten imagenes JPG, PNG o WebP.")

        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        if file_size <= 0:
            raise ImageUploadError("La imagen esta vacia.")
        if file_size > MAX_IMAGE_SIZE_BYTES:
            raise ImageUploadError("La imagen supera el tamano maximo permitido de 4 MB.")

        public_id = f"inventario-rey/products/{_safe_public_reference(reference)}/main"

        try:
            upload_result = cloudinary.uploader.upload(
                file,
                public_id=public_id,
                resource_type="image",
                overwrite=True,
                unique_filename=False,
                use_filename=False,
                invalidate=True,
            )
        except Exception as exc:
            raise ImageUploadError("No se pudo cargar la imagen a Cloudinary.") from exc

        stored_public_id = upload_result["public_id"]
        optimized_url, _ = cloudinary_url(
            stored_public_id,
            secure=True,
            fetch_format="auto",
            quality="auto",
        )

        return UploadedImage(
            secure_url=upload_result["secure_url"],
            optimized_url=optimized_url,
            public_id=stored_public_id,
            width=int(upload_result["width"]),
            height=int(upload_result["height"]),
            format=str(upload_result["format"]),
            file_size=int(upload_result.get("bytes", file_size)),
        )
