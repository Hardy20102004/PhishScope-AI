from typing import Any, List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.api import deps
from app.schemas.cyber_os import (
    CyberOSOverview, PlatformRegistryEntryCreate, PlatformRegistryEntryResponse,
    PlatformRegistryEntryListResponse, UnifiedObservabilityMetricListResponse
)
from app.services.cyber_os.kernel import CyberOSKernel

router = APIRouter()

@router.get("/overview", response_model=CyberOSOverview)
def get_cyberos_overview(db: Session = Depends(deps.get_db)) -> Any:
    """Get high-level overview of the CyberOS Kernel."""
    kernel = CyberOSKernel(db)
    stats = kernel.get_kernel_overview()
    
    return CyberOSOverview(**stats)

@router.post("/registry", response_model=PlatformRegistryEntryResponse)
def register_module(
    *,
    db: Session = Depends(deps.get_db),
    entry_in: PlatformRegistryEntryCreate
) -> Any:
    """Register a new platform module."""
    kernel = CyberOSKernel(db)
    entry = kernel.registry.register_module(entry_in)
    return {
        "status": "success",
        "data": entry,
        "meta": {"request_id": "req-os-1", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/registry", response_model=PlatformRegistryEntryListResponse)
def get_registered_modules(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get all registered modules."""
    kernel = CyberOSKernel(db)
    modules = kernel.registry.get_registered_modules(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": modules,
        "meta": {"request_id": "req-os-2", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }

@router.get("/observability", response_model=UnifiedObservabilityMetricListResponse)
def get_observability_metrics(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """Get platform observability metrics."""
    kernel = CyberOSKernel(db)
    metrics = kernel.observability.get_metrics(skip=skip, limit=limit)
    return {
        "status": "success",
        "data": metrics,
        "meta": {"request_id": "req-os-3", "timestamp": datetime.now(timezone.utc).isoformat(), "version": "v1.0"}
    }
