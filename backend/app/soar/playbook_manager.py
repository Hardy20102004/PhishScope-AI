import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.soar import Playbook

class PlaybookManager:
    """
    Manages CRUD and versioning for SOAR Playbooks.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_playbook(self, name: str, description: str, tenant_id: uuid.UUID) -> Playbook:
        # Provide a default mock workflow payload for demonstration
        default_workflow = {
            "nodes": [
                {"id": "start", "type": "trigger", "label": "Incident Triggered"},
                {"id": "enrich", "type": "action", "label": "Enrich IPs (VirusTotal)"},
                {"id": "approval", "type": "approval", "label": "Wait for Analyst Approval"},
                {"id": "isolate", "type": "action", "label": "Isolate Host (CrowdStrike)"}
            ],
            "edges": [
                {"source": "start", "target": "enrich"},
                {"source": "enrich", "target": "approval"},
                {"source": "approval", "target": "isolate"}
            ]
        }
        
        playbook = Playbook(
            tenant_id=tenant_id,
            name=name,
            description=description,
            workflow_data=default_workflow,
            status="PUBLISHED"
        )
        self.db.add(playbook)
        await self.db.commit()
        await self.db.refresh(playbook)
        return playbook

    async def get_playbook(self, playbook_id: uuid.UUID) -> Playbook:
        result = await self.db.execute(select(Playbook).where(Playbook.id == playbook_id))
        return result.scalar_one_or_none()
