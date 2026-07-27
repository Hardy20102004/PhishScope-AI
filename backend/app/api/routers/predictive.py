from fastapi import APIRouter
from app.api.api_v1.endpoints import predictive

router = APIRouter()
router.include_router(predictive.router, tags=["Predictive Threat Intelligence"])
