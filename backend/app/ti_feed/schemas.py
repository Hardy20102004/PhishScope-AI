from typing import Optional, Dict, Any, List
from pydantic import ConfigDict, BaseModel, Field
import uuid
from datetime import datetime

from app.ti_feed.models import FeedFormat, FeedType, FeedStatus, SyncStatus

class FeedRegistryBase(BaseModel):
    name: str
    description: Optional[str] = None
    feed_type: FeedType
    format: FeedFormat
    source_uri: str
    auth_config: Optional[Dict[str, Any]] = None
    connector_config: Optional[Dict[str, Any]] = None
    sync_interval_minutes: int = 60
    is_enabled: bool = True

class FeedRegistryCreate(FeedRegistryBase):
    pass

class FeedRegistryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_enabled: Optional[bool] = None
    sync_interval_minutes: Optional[int] = None
    auth_config: Optional[Dict[str, Any]] = None
    connector_config: Optional[Dict[str, Any]] = None

class FeedRegistryResponse(FeedRegistryBase):
    id: uuid.UUID
    status: FeedStatus
    last_sync_at: Optional[datetime] = None
    next_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FeedVersionResponse(BaseModel):
    id: uuid.UUID
    feed_id: uuid.UUID
    version_hash: Optional[str]
    status: SyncStatus
    indicators_added: int
    indicators_updated: int
    errors_encountered: int
    started_at: datetime
    completed_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class FeedAnalytics(BaseModel):
    total_feeds: int
    active_feeds: int
    total_indicators_ingested: int
    sync_success_rate: float
    recent_errors: int
    feeds_by_format: Dict[str, int]
