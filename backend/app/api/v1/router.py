from fastapi import APIRouter

from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.catalogs import router as catalogs_router
from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.inventory import router as inventory_router
from backend.app.api.v1.products import router as products_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(catalogs_router)
api_router.include_router(health_router)
api_router.include_router(inventory_router)
api_router.include_router(products_router)
