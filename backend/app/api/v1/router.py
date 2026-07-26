"""Aggregates all v1 routers. New resource routers (products, sales, ...) register here."""

from fastapi import APIRouter

from app.api.v1.routes import auth, health, products, sales, settings

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(products.router)
api_router.include_router(sales.router)
api_router.include_router(settings.router)
