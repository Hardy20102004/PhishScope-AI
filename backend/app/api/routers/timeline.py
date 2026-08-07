from fastapi import APIRouter
from app.api.api_v1.endpoints import timeline

router = APIRouter()
router.include_router(timeline.router, tags=["Timeline Intelligence"])
