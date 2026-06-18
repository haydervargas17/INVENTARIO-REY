import os

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.constants import DEFAULT_COLORS
from backend.app.database import SessionLocal
from backend.app.models import Color, User, UserRole
from backend.app.security.password import hash_password
from backend.app.utils.text import normalize_catalog_value


def seed_colors(db: Session) -> int:
    created_count = 0

    for color_name in DEFAULT_COLORS:
        normalized_name = normalize_catalog_value(color_name)
        existing_color = db.scalar(
            select(Color).where(
                Color.normalized_name == normalized_name,
                Color.deleted_at.is_(None),
            )
        )

        if existing_color is not None:
            continue

        db.add(Color(name=color_name, normalized_name=normalized_name))
        created_count += 1

    return created_count


def seed_system_admin(db: Session) -> bool:
    username = os.getenv("SYSTEM_ADMIN_USERNAME")
    password = os.getenv("SYSTEM_ADMIN_PASSWORD")
    full_name = os.getenv("SYSTEM_ADMIN_FULL_NAME")

    if not username or not password or not full_name:
        return False

    existing_user = db.scalar(
        select(User).where(
            User.username == username,
            User.deleted_at.is_(None),
        )
    )

    if existing_user is not None:
        return False

    db.add(
        User(
            username=username,
            password_hash=hash_password(password),
            full_name=full_name,
            role=UserRole.SYSTEM_ADMIN,
        )
    )
    return True


def run_seed() -> None:
    with SessionLocal() as db:
        colors_created = seed_colors(db)
        system_admin_created = seed_system_admin(db)
        db.commit()

    print(f"Colors created: {colors_created}")
    print(f"System admin created: {system_admin_created}")


if __name__ == "__main__":
    run_seed()
