"""create initial schema

Revision ID: 8860d74903c1
Revises:
Create Date: 2026-06-18 00:04:37.194618+00:00
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "8860d74903c1"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.execute(
        "DO $$ BEGIN CREATE TYPE user_role AS ENUM ('system_admin', 'admin'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE location_type AS ENUM ('WAREHOUSE', 'STORE'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE movement_type AS ENUM ('IN', 'OUT', 'ADJUSTMENT'); "
        "EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )
    op.execute(
        "DO $$ BEGIN CREATE TYPE audit_action AS ENUM ("
        "'LOGIN', 'LOGOUT', 'CREATE', 'UPDATE', 'DELETE', "
        "'INVENTORY_IN', 'INVENTORY_OUT', 'INVENTORY_ADJUSTMENT', 'TOKEN_REVOKED'"
        "); EXCEPTION WHEN duplicate_object THEN NULL; END $$;"
    )

    user_role = postgresql.ENUM("system_admin", "admin", name="user_role", create_type=False)
    location_type = postgresql.ENUM("WAREHOUSE", "STORE", name="location_type", create_type=False)
    movement_type = postgresql.ENUM("IN", "OUT", "ADJUSTMENT", name="movement_type", create_type=False)
    audit_action = postgresql.ENUM(
        "LOGIN",
        "LOGOUT",
        "CREATE",
        "UPDATE",
        "DELETE",
        "INVENTORY_IN",
        "INVENTORY_OUT",
        "INVENTORY_ADJUSTMENT",
        "TOKEN_REVOKED",
        name="audit_action",
        create_type=False,
    )

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("username", sa.String(length=80), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=150), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "colors",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("normalized_name", sa.String(length=50), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "products",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("reference", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("brand", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("photo_url", sa.Text(), nullable=False),
        sa.Column("cloudinary_public_id", sa.String(length=255), nullable=True),
        sa.Column("current_purchase_price", sa.Integer(), nullable=False),
        sa.Column("current_sale_price", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column("updated_by", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("current_purchase_price >= 0", name="ck_products_purchase_price_non_negative"),
        sa.CheckConstraint("current_sale_price >= 0", name="ck_products_sale_price_non_negative"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "inventory_items",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("product_id", sa.UUID(), nullable=False),
        sa.Column("size", sa.Numeric(precision=4, scale=1), nullable=False),
        sa.Column("color_signature", sa.String(length=255), nullable=False),
        sa.Column("location_type", location_type, nullable=False),
        sa.Column("location_detail", sa.String(length=150), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("low_stock_threshold", sa.Integer(), server_default=sa.text("5"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_by", sa.UUID(), nullable=True),
        sa.Column("updated_by", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("size > 0", name="ck_inventory_items_size_positive"),
        sa.CheckConstraint("quantity >= 0", name="ck_inventory_items_quantity_non_negative"),
        sa.CheckConstraint(
            "low_stock_threshold >= 0",
            name="ck_inventory_items_low_stock_threshold_non_negative",
        ),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["updated_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "inventory_item_colors",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("inventory_item_id", sa.UUID(), nullable=False),
        sa.Column("color_id", sa.UUID(), nullable=False),
        sa.Column("sort_order", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["color_id"], ["colors.id"]),
        sa.ForeignKeyConstraint(["inventory_item_id"], ["inventory_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "inventory_movements",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("inventory_item_id", sa.UUID(), nullable=False),
        sa.Column("movement_type", movement_type, nullable=False),
        sa.Column("quantity_delta", sa.Integer(), nullable=False),
        sa.Column("previous_quantity", sa.Integer(), nullable=False),
        sa.Column("new_quantity", sa.Integer(), nullable=False),
        sa.Column("purchase_unit_price", sa.Integer(), nullable=True),
        sa.Column("sale_unit_price", sa.Integer(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("quantity_delta <> 0", name="ck_inventory_movements_quantity_delta_not_zero"),
        sa.CheckConstraint("previous_quantity >= 0", name="ck_inventory_movements_previous_quantity_non_negative"),
        sa.CheckConstraint("new_quantity >= 0", name="ck_inventory_movements_new_quantity_non_negative"),
        sa.CheckConstraint(
            "purchase_unit_price IS NULL OR purchase_unit_price >= 0",
            name="ck_inventory_movements_purchase_price_non_negative",
        ),
        sa.CheckConstraint(
            "sale_unit_price IS NULL OR sale_unit_price >= 0",
            name="ck_inventory_movements_sale_price_non_negative",
        ),
        sa.CheckConstraint(
            "(movement_type = 'IN' AND quantity_delta > 0) OR "
            "(movement_type = 'OUT' AND quantity_delta < 0) OR "
            "(movement_type = 'ADJUSTMENT')",
            name="ck_inventory_movements_delta_matches_type",
        ),
        sa.ForeignKeyConstraint(["inventory_item_id"], ["inventory_items.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("action", audit_action, nullable=False),
        sa.Column("entity_name", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.UUID(), nullable=True),
        sa.Column("ip_address", postgresql.INET(), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "revoked_tokens",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("token_jti", sa.String(length=120), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=120), server_default=sa.text("'logout'"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ux_users_username_active",
        "users",
        [sa.text("lower(username)")],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ux_colors_normalized_name_active",
        "colors",
        ["normalized_name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ux_products_reference_active",
        "products",
        [sa.text("upper(reference)")],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_products_search",
        "products",
        [sa.text("upper(reference)"), sa.text("lower(name)")],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ux_inventory_items_unique_active",
        "inventory_items",
        [
            "product_id",
            "size",
            "color_signature",
            "location_type",
            sa.text("lower(location_detail)"),
        ],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_items_product",
        "inventory_items",
        ["product_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_items_filters",
        "inventory_items",
        ["size", "location_type", "quantity"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_items_low_stock",
        "inventory_items",
        ["quantity", "low_stock_threshold"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ux_inventory_item_colors_active",
        "inventory_item_colors",
        ["inventory_item_id", "color_id"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_item_colors_color",
        "inventory_item_colors",
        ["color_id"],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_movements_item_created",
        "inventory_movements",
        ["inventory_item_id", sa.text("created_at DESC")],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_movements_user_created",
        "inventory_movements",
        ["user_id", sa.text("created_at DESC")],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index(
        "ix_inventory_movements_type_created",
        "inventory_movements",
        ["movement_type", sa.text("created_at DESC")],
        postgresql_where=sa.text("deleted_at IS NULL"),
    )
    op.create_index("ix_audit_logs_user_created", "audit_logs", ["user_id", sa.text("created_at DESC")])
    op.create_index("ix_audit_logs_action_created", "audit_logs", ["action", sa.text("created_at DESC")])
    op.create_index("ix_audit_logs_entity", "audit_logs", ["entity_name", "entity_id"])
    op.create_index("ux_revoked_tokens_jti", "revoked_tokens", ["token_jti"], unique=True)
    op.create_index("ix_revoked_tokens_user", "revoked_tokens", ["user_id"])
    op.create_index("ix_revoked_tokens_expires_at", "revoked_tokens", ["expires_at"])


def downgrade() -> None:
    op.drop_index("ix_revoked_tokens_expires_at", table_name="revoked_tokens")
    op.drop_index("ix_revoked_tokens_user", table_name="revoked_tokens")
    op.drop_index("ux_revoked_tokens_jti", table_name="revoked_tokens")
    op.drop_index("ix_audit_logs_entity", table_name="audit_logs")
    op.drop_index("ix_audit_logs_action_created", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_created", table_name="audit_logs")
    op.drop_index("ix_inventory_movements_type_created", table_name="inventory_movements")
    op.drop_index("ix_inventory_movements_user_created", table_name="inventory_movements")
    op.drop_index("ix_inventory_movements_item_created", table_name="inventory_movements")
    op.drop_index("ix_inventory_item_colors_color", table_name="inventory_item_colors")
    op.drop_index("ux_inventory_item_colors_active", table_name="inventory_item_colors")
    op.drop_index("ix_inventory_items_low_stock", table_name="inventory_items")
    op.drop_index("ix_inventory_items_filters", table_name="inventory_items")
    op.drop_index("ix_inventory_items_product", table_name="inventory_items")
    op.drop_index("ux_inventory_items_unique_active", table_name="inventory_items")
    op.drop_index("ix_products_search", table_name="products")
    op.drop_index("ux_products_reference_active", table_name="products")
    op.drop_index("ux_colors_normalized_name_active", table_name="colors")
    op.drop_index("ux_users_username_active", table_name="users")

    op.drop_table("revoked_tokens")
    op.drop_table("audit_logs")
    op.drop_table("inventory_movements")
    op.drop_table("inventory_item_colors")
    op.drop_table("inventory_items")
    op.drop_table("products")
    op.drop_table("colors")
    op.drop_table("users")

    bind = op.get_bind()
    postgresql.ENUM(name="audit_action").drop(bind, checkfirst=True)
    postgresql.ENUM(name="movement_type").drop(bind, checkfirst=True)
    postgresql.ENUM(name="location_type").drop(bind, checkfirst=True)
    postgresql.ENUM(name="user_role").drop(bind, checkfirst=True)
