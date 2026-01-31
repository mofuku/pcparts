"""API routers."""

from fastapi import APIRouter

from app.api import parts, prices, builds, health

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(parts.router, prefix="/parts", tags=["parts"])
router.include_router(prices.router, prefix="/prices", tags=["prices"])
router.include_router(builds.router, prefix="/builds", tags=["builds"])
