from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class IncidentSchema(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    severity: str
    status: str
    component: str
    metadata_json: dict
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class SystemMetricSchema(BaseModel):
    id: UUID
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    tags_json: dict

    model_config = ConfigDict(from_attributes=True)
