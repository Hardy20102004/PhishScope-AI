import structlog
from sqlalchemy.orm import Session
from app.models.rag import KnowledgeAsset, KnowledgeAssetStatus
from typing import Optional, List

logger = structlog.get_logger("phoenix.rag.governance")

class KnowledgeManager:
    def __init__(self, db: Session):
        self.db = db

    def get_asset(self, asset_id: str) -> Optional[KnowledgeAsset]:
        return self.db.query(KnowledgeAsset).filter(KnowledgeAsset.id == asset_id).first()

    def list_assets(self, tenant_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[KnowledgeAsset]:
        query = self.db.query(KnowledgeAsset)
        if tenant_id:
            query = query.filter(KnowledgeAsset.tenant_id == tenant_id)
        return query.order_by(KnowledgeAsset.created_at.desc()).offset(skip).limit(limit).all()

    def update_status(self, asset_id: str, new_status: KnowledgeAssetStatus) -> Optional[KnowledgeAsset]:
        asset = self.get_asset(asset_id)
        if asset:
            logger.info("updating_asset_status", asset_id=asset_id, old_status=asset.status, new_status=new_status)
            asset.status = new_status
            self.db.commit()
            self.db.refresh(asset)
        return asset

    def delete_asset(self, asset_id: str) -> bool:
        asset = self.get_asset(asset_id)
        if asset:
            logger.info("deleting_asset", asset_id=asset_id)
            self.db.delete(asset)
            self.db.commit()
            return True
        return False
