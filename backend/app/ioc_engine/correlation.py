import uuid
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from loguru import logger

from app.models.threat_intel import Indicator, IOCType, IndicatorCorrelation, CorrelationEvidence
from app.ioc_engine.normalization import NormalizationEngine
from app.ioc_engine.similarity import SimilarityEngine
from app.ioc_engine.relationship import RelationshipEngine
from app.ioc_engine.confidence import ConfidenceEngine
from app.ioc_engine.evidence import EvidenceEngine
from app.ioc_engine.schemas import IndicatorCreate, IndicatorResponse
from app.ioc_engine.kg_sync import KGSyncService

class IOCCorrelationEngine:
    """
    Central orchestrator for the Enterprise IOC Correlation Engine.
    Handles ingestion, normalization, relationship discovery, and scoring.
    """

    def __init__(self, db: Session):
        self.db = db
        self.relationship_engine = RelationshipEngine(db)
        self.evidence_engine = EvidenceEngine(db)
        self.kg_sync = KGSyncService(db)

    def ingest_indicator(self, data: IndicatorCreate) -> Indicator:
        """
        Ingests a new IOC, normalizes it, and starts the correlation process.
        """
        # 1. Normalization
        canonical_value, norm_metadata = NormalizationEngine.normalize(data.value, data.type)
        
        # 2. Check if indicator already exists (by canonical value)
        existing_indicator = self.db.query(Indicator).filter(
            Indicator.normalized_value == canonical_value,
            Indicator.type == data.type
        ).first()

        if existing_indicator:
            # Update observation count and context
            existing_indicator.observation_count += 1
            # Merge context (simplified)
            if existing_indicator.raw_context and data.raw_context:
                existing_indicator.raw_context.update(data.raw_context)
            elif data.raw_context:
                existing_indicator.raw_context = data.raw_context
                
            self.db.commit()
            self.db.refresh(existing_indicator)
            
            # Still run correlation to see if new context creates new links
            self.correlate(existing_indicator)
            return existing_indicator
            
        # 3. Create new indicator
        new_indicator = Indicator(
            value=data.value,
            type=data.type,
            normalized_value=canonical_value,
            source_module=data.source_module,
            raw_context=data.raw_context,
            normalization_metadata=norm_metadata
        )
        
        self.db.add(new_indicator)
        self.db.commit()
        self.db.refresh(new_indicator)
        
        # 4. Sync to Knowledge Graph
        self.kg_sync.sync_indicator(new_indicator)
        
        # 5. Trigger Correlation (Ideally async via Celery/RabbitMQ in production)
        self.correlate(new_indicator)
        
        return new_indicator
        
    def correlate(self, indicator: Indicator) -> None:
        """
        Runs the correlation pipeline for a specific indicator.
        """
        logger.info(f"Starting correlation for IOC: {indicator.value} ({indicator.type})")
        
        # 1. Discover Relationships
        relationships = self.relationship_engine.discover_relationships(indicator)
        
        for rel in relationships:
            # 2. Generate Evidence for the relationship
            # In a real system, the relationship engine would return the evidence data along with the relationship
            evidence = self.evidence_engine.generate_evidence(
                relationship=rel,
                source_system="Internal Correlation Engine",
                description=f"Discovered {rel.correlation_type} between {indicator.value} and related entity.",
                data={"method": "heuristic"}
            )
            
            # 3. Calculate Confidence
            # Retrieve all evidence for this relationship
            all_evidence = self.db.query(CorrelationEvidence).filter(CorrelationEvidence.relationship_id == rel.id).all()
            new_confidence = ConfidenceEngine.calculate_confidence(rel, all_evidence)
            
            rel.confidence = new_confidence
            self.db.add(rel)
            
            # 4. Sync Relationship to Knowledge Graph
            if rel.target_indicator_id:
                target_indicator = self.db.query(Indicator).filter(Indicator.id == rel.target_indicator_id).first()
                if target_indicator:
                    self.kg_sync.sync_relationship(rel, indicator, target_indicator)
            
        self.db.commit()
        logger.info(f"Finished correlation for IOC: {indicator.value}. Found {len(relationships)} relationships.")

