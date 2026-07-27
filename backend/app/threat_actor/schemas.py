from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field
import uuid
from datetime import datetime

from app.threat_actor.models import ThreatActorStatus

class ActorAliasBase(BaseModel):
    alias_name: str
    source: Optional[str] = None

class ActorAliasResponse(ActorAliasBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class TTPAssociationBase(BaseModel):
    mitre_id: str
    tactic: Optional[str] = None
    technique_name: Optional[str] = None

class TTPAssociationResponse(TTPAssociationBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class InfrastructureAssociationBase(BaseModel):
    indicator_id: uuid.UUID
    usage: Optional[str] = None

class InfrastructureAssociationResponse(InfrastructureAssociationBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class MalwareAssociationBase(BaseModel):
    malware_family: str
    role: Optional[str] = None

class MalwareAssociationResponse(MalwareAssociationBase):
    id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

class ThreatActorBase(BaseModel):
    name: str
    description: Optional[str] = None
    motivations: Optional[List[str]] = None
    objectives: Optional[List[str]] = None
    target_sectors: Optional[List[str]] = None
    target_regions: Optional[List[str]] = None
    status: ThreatActorStatus = ThreatActorStatus.UNKNOWN

class ThreatActorCreate(ThreatActorBase):
    pass

class ThreatActorUpdate(BaseModel):
    description: Optional[str] = None
    motivations: Optional[List[str]] = None
    status: Optional[ThreatActorStatus] = None

class ThreatActorResponse(ThreatActorBase):
    id: uuid.UUID
    first_observed: Optional[datetime]
    last_observed: Optional[datetime]
    confidence: float
    aliases: List[ActorAliasResponse] = []
    ttp_associations: List[TTPAssociationResponse] = []
    malware: List[MalwareAssociationResponse] = []
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AttributionEvidenceBase(BaseModel):
    actor_id: uuid.UUID
    reference_id: Optional[uuid.UUID] = None
    reference_type: Optional[str] = None
    is_observed_fact: bool
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)

class AttributionEvidenceResponse(AttributionEvidenceBase):
    id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

