from sqlalchemy.orm import Session
from app.threat_actor.models import ThreatActor, ThreatActorStatus
from app.threat_actor.schemas import ThreatActorCreate, ThreatActorUpdate
import uuid

class ProfileEngine:
    def __init__(self, db: Session):
        self.db = db

    def create_actor(self, data: ThreatActorCreate) -> ThreatActor:
        actor = ThreatActor(**data.model_dump())
        self.db.add(actor)
        self.db.commit()
        self.db.refresh(actor)
        return actor

    def get_actor(self, actor_id: uuid.UUID) -> ThreatActor:
        return self.db.query(ThreatActor).filter(ThreatActor.id == actor_id).first()

    def update_actor(self, actor_id: uuid.UUID, data: ThreatActorUpdate) -> ThreatActor:
        actor = self.get_actor(actor_id)
        if not actor:
            raise ValueError("Actor not found")
            
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(actor, key, value)
            
        self.db.commit()
        self.db.refresh(actor)
        return actor
