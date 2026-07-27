from sqlalchemy.orm import Session
from app.threat_actor.models import TTPAssociation
import uuid

class MitreMapper:
    """
    Handles association of MITRE ATT&CK TTPs to Threat Actors.
    """
    def __init__(self, db: Session):
        self.db = db

    def add_ttp(self, actor_id: uuid.UUID, mitre_id: str, tactic: str = None, technique_name: str = None) -> TTPAssociation:
        """
        Adds a MITRE ATT&CK association. In a real system, this would query a local ATT&CK bundle to validate `mitre_id`.
        """
        ttp = TTPAssociation(
            actor_id=actor_id,
            mitre_id=mitre_id,
            tactic=tactic,
            technique_name=technique_name
        )
        self.db.add(ttp)
        self.db.commit()
        self.db.refresh(ttp)
        return ttp

    def get_ttps(self, actor_id: uuid.UUID):
        return self.db.query(TTPAssociation).filter(TTPAssociation.actor_id == actor_id).all()
