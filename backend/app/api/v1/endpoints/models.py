from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api import deps
from app.model_manager.registry import ModelRegistryService
from app.model_manager.router import RoutingEngine
from app.models.model_manager import AIModel, AIProvider, ModelCostLog, RoutingPolicy
from app.schemas.model_manager import (
    AIModelCreate,
    AIModelResponse,
    AIProviderCreate,
    AIProviderResponse,
    ModelCostLogResponse,
    RoutingPolicyCreate,
    RoutingPolicyResponse,
    RoutingRequest,
    RoutingResponse,
)

router = APIRouter()

# --- Providers ---
@router.get("/providers", response_model=List[AIProviderResponse])
def get_providers(db: Session = Depends(deps.get_db)):
    return db.query(AIProvider).all()

@router.post("/providers", response_model=AIProviderResponse)
def create_provider(req: AIProviderCreate, db: Session = Depends(deps.get_db)):
    service = ModelRegistryService(db)
    return service.register_provider(req)

# --- Models ---
@router.get("/inventory", response_model=List[AIModelResponse])
def get_models(db: Session = Depends(deps.get_db)):
    return db.query(AIModel).all()

@router.post("/inventory", response_model=AIModelResponse)
def create_model(req: AIModelCreate, db: Session = Depends(deps.get_db)):
    service = ModelRegistryService(db)
    return service.register_model(req)

# --- Routing Policies ---
@router.get("/policies", response_model=List[RoutingPolicyResponse])
def get_policies(db: Session = Depends(deps.get_db)):
    return db.query(RoutingPolicy).all()

@router.post("/policies", response_model=RoutingPolicyResponse)
def create_policy(req: RoutingPolicyCreate, db: Session = Depends(deps.get_db)):
    policy = RoutingPolicy(**req.model_dump())
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy

@router.post("/route", response_model=RoutingResponse)
def route_task(req: RoutingRequest, db: Session = Depends(deps.get_db)):
    engine = RoutingEngine(db)
    try:
        return engine.get_model_for_task(req.capability)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# --- Cost & Analytics ---
@router.get("/costs", response_model=List[ModelCostLogResponse])
def get_costs(limit: int = 100, db: Session = Depends(deps.get_db)):
    return db.query(ModelCostLog).order_by(ModelCostLog.timestamp.desc()).limit(limit).all()

@router.get("/costs/summary")
def get_cost_summary(db: Session = Depends(deps.get_db)):
    total = db.query(func.sum(ModelCostLog.total_cost)).scalar() or 0.0
    return {"total_cost": total}
