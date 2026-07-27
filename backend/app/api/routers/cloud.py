from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    cloud_tenants,
    cloud_workspaces,
    cloud_federation,
    cloud_sharing,
    cloud_sync,
    cloud_analytics
)

router = APIRouter()

router.include_router(cloud_tenants.router, prefix="/tenants", tags=["Cloud Tenants"])
router.include_router(cloud_workspaces.router, prefix="/workspaces", tags=["Cloud Workspaces"])
router.include_router(cloud_federation.router, prefix="/federation", tags=["Cloud Federation"])
router.include_router(cloud_sharing.router, prefix="/sharing", tags=["Cloud Sharing"])
router.include_router(cloud_sync.router, prefix="/sync", tags=["Cloud Synchronization"])
router.include_router(cloud_analytics.router, prefix="/analytics", tags=["Cloud Analytics"])
