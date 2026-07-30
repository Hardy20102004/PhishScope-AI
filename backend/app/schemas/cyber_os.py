from typing import Any, Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.base import APIResponse
from app.models.cyber_os import OSComponentStatus

class PlatformRegistryEntryBase(BaseModel):
    module_name: str
    version: str
    api_endpoint_prefix: str
    capabilities: List[str] = Field(default_factory=list)
    status: OSComponentStatus = OSComponentStatus.ONLINE

class PlatformRegistryEntryCreate(PlatformRegistryEntryBase):
    pass

class PlatformRegistryEntry(PlatformRegistryEntryBase):
    id: UUID
    registered_at: datetime
    last_heartbeat: datetime

    class Config:
        orm_mode = True

class UnifiedObservabilityMetricBase(BaseModel):
    metric_type: str
    value: float
    unit: str
    source_module: str

class UnifiedObservabilityMetricCreate(UnifiedObservabilityMetricBase):
    pass

class UnifiedObservabilityMetric(UnifiedObservabilityMetricBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True

class GlobalSystemLogBase(BaseModel):
    severity: str
    source_module: str
    message: str
    context_data: Dict[str, Any] = Field(default_factory=dict)

class GlobalSystemLogCreate(GlobalSystemLogBase):
    pass

class GlobalSystemLog(GlobalSystemLogBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True

class CyberOSOverview(BaseModel):
    kernel_status: str
    registered_modules_count: int
    global_cpu_usage: float
    global_memory_usage: float
    active_alerts: int
    ai_status: str

class PlatformRegistryEntryResponse(APIResponse[PlatformRegistryEntry]):
    pass

class PlatformRegistryEntryListResponse(APIResponse[List[PlatformRegistryEntry]]):
    pass

class UnifiedObservabilityMetricListResponse(APIResponse[List[UnifiedObservabilityMetric]]):
    pass
