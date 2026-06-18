from enum import StrEnum


class UserRole(StrEnum):
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"


class LocationType(StrEnum):
    WAREHOUSE = "WAREHOUSE"
    STORE = "STORE"


class MovementType(StrEnum):
    IN = "IN"
    OUT = "OUT"
    ADJUSTMENT = "ADJUSTMENT"


class AuditAction(StrEnum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    INVENTORY_IN = "INVENTORY_IN"
    INVENTORY_OUT = "INVENTORY_OUT"
    INVENTORY_ADJUSTMENT = "INVENTORY_ADJUSTMENT"
    TOKEN_REVOKED = "TOKEN_REVOKED"


def enum_values(enum_class: type[StrEnum]) -> list[str]:
    return [member.value for member in enum_class]
