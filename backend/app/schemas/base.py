from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class PaginationMeta(BaseModel):
    page: int = Field(..., json_schema_extra={"example": 1})
    size: int = Field(..., json_schema_extra={"example": 20})
    total_items: int = Field(..., json_schema_extra={"example": 100})
    total_pages: int = Field(..., json_schema_extra={"example": 5})
    has_next: bool = Field(..., json_schema_extra={"example": True})
    has_previous: bool = Field(..., json_schema_extra={"example": False})
    next_cursor: Optional[str] = Field(None, json_schema_extra={"example": "eyJpZCI6IDEwfQ=="})

class ResponseMeta(BaseModel):
    request_id: str = Field(..., json_schema_extra={"example": "uuid-1234"})
    timestamp: str = Field(..., json_schema_extra={"example": "2026-07-24T12:00:00Z"})
    version: str = Field("v1.0")
    pagination: Optional[PaginationMeta] = None

class ErrorDetail(BaseModel):
    field: Optional[str] = Field(None, json_schema_extra={"example": "email"})
    issue: str = Field(..., json_schema_extra={"example": "Invalid format"})

class ErrorPayload(BaseModel):
    code: str = Field(..., json_schema_extra={"example": "VALIDATION_FAILED"})
    message: str = Field(..., json_schema_extra={"example": "Input validation failed"})
    details: Optional[List[ErrorDetail]] = None

class APIResponse(BaseModel, Generic[DataT]):
    """Standard generic wrapper for all successful API responses."""
    status: str = Field("success", json_schema_extra={"example": "success"})
    data: DataT
    meta: ResponseMeta

class APIErrorResponse(BaseModel):
    """Standard wrapper for all failed API responses."""
    status: str = Field("error", json_schema_extra={"example": "error"})
    error: ErrorPayload
    meta: ResponseMeta
