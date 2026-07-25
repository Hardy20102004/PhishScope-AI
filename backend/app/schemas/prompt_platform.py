from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime
from app.models.prompt_platform import PromptLifecycleState

class PromptVersionBase(BaseModel):
    version_number: str
    system_prompt: str
    user_template: str
    required_variables: List[str] = []
    lifecycle_state: PromptLifecycleState = PromptLifecycleState.DRAFT

class PromptVersionCreate(PromptVersionBase):
    pass

class PromptVersionResponse(PromptVersionBase):
    id: str
    template_id: str
    model_config = ConfigDict(from_attributes=True)

class PromptTemplateBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    owner: str = "system"

class PromptTemplateCreate(PromptTemplateBase):
    pass

class PromptTemplateResponse(PromptTemplateBase):
    id: str
    is_active: bool
    versions: List[PromptVersionResponse] = []
    model_config = ConfigDict(from_attributes=True)

class PromptComposeRequest(BaseModel):
    template_name: str
    variables: Dict[str, Any]
    provider: str = "openai"

class PromptComposeResponse(BaseModel):
    system_prompt: str
    user_prompt: str
    provider_formatted: Any # E.g. array of messages for OpenAI, or string for others
    version_used: str
    tokens_estimated: int
