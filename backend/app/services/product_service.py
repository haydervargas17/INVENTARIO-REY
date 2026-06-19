from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models import AuditAction, Product
from backend.app.repositories.audit_repository import AuditRepository
from backend.app.repositories.product_repository import ProductRepository
from backend.app.services.cloudinary_service import CloudinaryImageService, UploadedImage
from backend.app.schemas.product import ProductCreate, ProductUpdate


class ProductConflictError(Exception):
    """Raised when a product reference already exists."""


class ProductNotFoundError(Exception):
    """Raised when a product is not found."""


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.products = ProductRepository(db)
        self.audit_logs = AuditRepository(db)

    def list_products(self, search: str | None = None, limit: int = 50, offset: int = 0) -> list[Product]:
        return self.products.list(search=search, limit=limit, offset=offset)

    def create_product(self, payload: ProductCreate, user_id: UUID) -> Product:
        existing_product = self.products.get_by_reference(payload.reference)
        if existing_product is not None:
            raise ProductConflictError("Product reference already exists.")

        product = self.products.create(payload, user_id=user_id)
        self.db.flush()
        self.audit_logs.create(
            action=AuditAction.CREATE,
            user_id=user_id,
            entity_name="products",
            entity_id=product.id,
            metadata={"reference": product.reference},
        )
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_product(self, product_id: UUID, payload: ProductUpdate, user_id: UUID) -> Product:
        product = self.products.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError("Product not found.")

        self.products.update(product, payload, user_id=user_id)
        self.audit_logs.create(
            action=AuditAction.UPDATE,
            user_id=user_id,
            entity_name="products",
            entity_id=product.id,
            metadata={"reference": product.reference},
        )
        self.db.commit()
        self.db.refresh(product)
        return product

    def upload_product_image(
        self,
        *,
        product_id: UUID,
        file,
        content_type: str | None,
        user_id: UUID,
    ) -> tuple[Product, UploadedImage]:
        product = self.products.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError("Product not found.")

        uploaded_image = CloudinaryImageService().upload_product_image(
            reference=product.reference,
            file=file,
            content_type=content_type,
        )
        self.products.update_image(
            product,
            photo_url=uploaded_image.optimized_url,
            cloudinary_public_id=uploaded_image.public_id,
            user_id=user_id,
        )
        self.audit_logs.create(
            action=AuditAction.UPDATE,
            user_id=user_id,
            entity_name="products",
            entity_id=product.id,
            metadata={
                "reference": product.reference,
                "image_public_id": uploaded_image.public_id,
            },
        )
        self.db.commit()
        self.db.refresh(product)
        return product, uploaded_image
