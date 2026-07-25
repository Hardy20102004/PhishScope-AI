from typing import List, Optional

import structlog
from sqlalchemy.orm import Session

from app.models.prompt_platform import PromptLifecycleState, PromptTemplate, PromptVersion

logger = structlog.get_logger("phoenix.prompt_platform.registry")

class PromptRegistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_template(self, template_name: str) -> Optional[PromptTemplate]:
        return self.db.query(PromptTemplate).filter(PromptTemplate.name == template_name).first()

    def get_active_version(self, template_name: str) -> Optional[PromptVersion]:
        template = self.get_template(template_name)
        if not template:
            return None
        
        # Prefer published
        published = next((v for v in template.versions if v.lifecycle_state == PromptLifecycleState.PUBLISHED.value), None)
        if published:
            return published
        
        # Fallback to approved
        approved = next((v for v in template.versions if v.lifecycle_state == PromptLifecycleState.APPROVED.value), None)
        if approved:
            return approved
            
        # Fallback to latest draft
        drafts = [v for v in template.versions if v.lifecycle_state == PromptLifecycleState.DRAFT.value]
        if drafts:
            # simple mock logic to return last element, assuming it was added last
            return drafts[-1]
            
        return None

    def create_template(self, name: str, category: str, description: str = "") -> PromptTemplate:
        template = self.get_template(name)
        if template:
            return template
            
        template = PromptTemplate(
            name=name,
            category=category,
            description=description,
            owner="system"
        )
        self.db.add(template)
        self.db.commit()
        self.db.refresh(template)
        return template

    def create_version(self, template_id: str, version_number: str, system_prompt: str, user_template: str, required_variables: List[str]) -> PromptVersion:
        version = PromptVersion(
            template_id=template_id,
            version_number=version_number,
            system_prompt=system_prompt,
            user_template=user_template,
            required_variables=required_variables,
            lifecycle_state=PromptLifecycleState.PUBLISHED.value
        )
        self.db.add(version)
        self.db.commit()
        self.db.refresh(version)
        return version
