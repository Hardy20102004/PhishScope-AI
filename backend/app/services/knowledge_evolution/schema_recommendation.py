from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.knowledge_evolution import SchemaRecommendation, ApprovalStatus
from app.schemas.knowledge_evolution import SchemaRecommendationCreate

class SchemaRecommendationEngine:
    def __init__(self, db: Session):
        self.db = db

    def generate_recommendation(self, rec_in: SchemaRecommendationCreate) -> SchemaRecommendation:
        db_rec = SchemaRecommendation(
            target_node_id=rec_in.target_node_id,
            recommendation_type=rec_in.recommendation_type,
            description=rec_in.description,
            evidence=rec_in.evidence,
            status=ApprovalStatus.PENDING
        )
        self.db.add(db_rec)
        self.db.commit()
        self.db.refresh(db_rec)
        return db_rec
        
    def get_pending_recommendations(self) -> List[SchemaRecommendation]:
        return self.db.query(SchemaRecommendation).filter(
            SchemaRecommendation.status == ApprovalStatus.PENDING
        ).all()
        
    def resolve_recommendation(self, rec_id: UUID, approved: bool) -> Optional[SchemaRecommendation]:
        db_rec = self.db.query(SchemaRecommendation).filter(SchemaRecommendation.id == rec_id).first()
        if db_rec:
            db_rec.status = ApprovalStatus.APPROVED if approved else ApprovalStatus.REJECTED
            self.db.add(db_rec)
            self.db.commit()
            self.db.refresh(db_rec)
        return db_rec
