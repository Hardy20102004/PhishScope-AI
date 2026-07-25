from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.schemas.prompt_platform import (
    PromptTemplateResponse, 
    PromptTemplateCreate,
    PromptVersionResponse,
    PromptVersionCreate,
    PromptComposeRequest,
    PromptComposeResponse
)
from app.prompt_platform.registry import PromptRegistryService
from app.prompt_platform.composer import PromptComposer
from app.prompt_platform.validator import PromptValidator
from app.prompt_platform.provider import ProviderAdapter
from app.models.prompt_platform import PromptTemplate, PromptVersion

router = APIRouter()

@router.get("/", response_model=List[PromptTemplateResponse])
def list_templates(db: Session = Depends(deps.get_db)):
    """List all prompt templates with their versions."""
    templates = db.query(PromptTemplate).all()
    return templates

@router.post("/", response_model=PromptTemplateResponse)
def create_template(req: PromptTemplateCreate, db: Session = Depends(deps.get_db)):
    """Create a new prompt template."""
    registry = PromptRegistryService(db)
    template = registry.create_template(req.name, req.category, req.description or "")
    return template

@router.post("/{template_id}/versions", response_model=PromptVersionResponse)
def create_version(template_id: str, req: PromptVersionCreate, db: Session = Depends(deps.get_db)):
    """Create a new version for a template."""
    registry = PromptRegistryService(db)
    version = registry.create_version(
        template_id=template_id,
        version_number=req.version_number,
        system_prompt=req.system_prompt,
        user_template=req.user_template,
        required_variables=req.required_variables
    )
    return version

@router.post("/compose", response_model=PromptComposeResponse)
def compose_prompt(req: PromptComposeRequest, db: Session = Depends(deps.get_db)):
    """
    Dynamically compose a prompt using Jinja2, validate it, and adapt for the provider.
    """
    registry = PromptRegistryService(db)
    version = registry.get_active_version(req.template_name)
    
    if not version:
        raise HTTPException(status_code=404, detail=f"No active version found for template {req.template_name}")
        
    validator = PromptValidator()
    # 1. Validate variables
    missing_vars = validator.validate_variables(version.required_variables, req.variables)
    if missing_vars:
        raise HTTPException(status_code=400, detail=f"Missing required variables: {missing_vars}")
        
    composer = PromptComposer()
    try:
        # 2. Render templates
        rendered_sys, rendered_user = composer.compose(
            system_template=version.system_prompt,
            user_template=version.user_template,
            variables=req.variables
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
    # 3. Validate rendered output limits & security
    is_valid, errors = validator.validate_rendered_prompt(rendered_sys, rendered_user)
    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Prompt validation failed: {errors}")
        
    # 4. Adapt for provider
    provider_format = ProviderAdapter.format_for_provider(rendered_sys, rendered_user, req.provider)
    
    # 5. Estimate final tokens
    estimated = validator.estimate_tokens(rendered_sys) + validator.estimate_tokens(rendered_user)
    
    return PromptComposeResponse(
        system_prompt=rendered_sys,
        user_prompt=rendered_user,
        provider_formatted=provider_format,
        version_used=version.version_number,
        tokens_estimated=estimated
    )
