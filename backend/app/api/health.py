"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {"status": "healthy"}


@router.get("/")
async def root():
    """API root."""
    return {
        "name": "PCParts API",
        "version": "0.1.0",
        "docs": "/docs",
    }
