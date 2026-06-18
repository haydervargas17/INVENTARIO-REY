from uuid import UUID

from sqlalchemy.orm import Session

from backend.app.models import AuditAction, Product
from backend.app.repositories.audit_repository import AuditRepository
from backend.app.repositories.product_repository import ProductRepository
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
