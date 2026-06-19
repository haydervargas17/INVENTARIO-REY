from uuid import UUID

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from backend.app.models import Product
from backend.app.schemas.product import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, product_id: UUID) -> Product | None:
        return self.db.scalar(
            select(Product).where(Product.id == product_id, Product.deleted_at.is_(None))
        )

    def get_by_reference(self, reference: str) -> Product | None:
        return self.db.scalar(
            select(Product).where(
                func.upper(Product.reference) == reference.strip().upper(),
                Product.deleted_at.is_(None),
            )
        )

    def list(self, search: str | None = None, limit: int = 50, offset: int = 0) -> list[Product]:
        stmt = select(Product).where(Product.deleted_at.is_(None)).order_by(Product.reference)

        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    Product.reference.ilike(pattern),
                    Product.name.ilike(pattern),
                    Product.description.ilike(pattern),
                    Product.brand.ilike(pattern),
                )
            )

        return list(self.db.scalars(stmt.limit(limit).offset(offset)))

    def create(self, payload: ProductCreate, user_id: UUID | None = None) -> Product:
        product = Product(
            reference=payload.reference.strip(),
            name=payload.name.strip(),
            brand=payload.brand.strip(),
            description=payload.description.strip(),
            photo_url=payload.photo_url.strip(),
            cloudinary_public_id=payload.cloudinary_public_id,
            current_purchase_price=payload.current_purchase_price,
            current_sale_price=payload.current_sale_price,
            created_by=user_id,
            updated_by=user_id,
        )
        self.db.add(product)
        return product

    def update(self, product: Product, payload: ProductUpdate, user_id: UUID | None = None) -> Product:
        update_data = payload.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if isinstance(value, str):
                value = value.strip()
            setattr(product, field, value)

        product.updated_by = user_id
        return product

    def update_prices(self, product: Product, purchase_price: int, sale_price: int, user_id: UUID | None) -> Product:
        product.current_purchase_price = purchase_price
        product.current_sale_price = sale_price
        product.updated_by = user_id
        return product

    def update_image(
        self,
        product: Product,
        *,
        photo_url: str,
        cloudinary_public_id: str,
        user_id: UUID | None,
    ) -> Product:
        product.photo_url = photo_url
        product.cloudinary_public_id = cloudinary_public_id
        product.updated_by = user_id
        return product
